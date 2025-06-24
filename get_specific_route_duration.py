import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

database_password = os.getenv('database_password')

query= '''select latest.origin, latest.destination, time_taken_secs latest_time, 1.0*time_taken_secs/historical_average pct_change  from
(select traffic_data.origin, traffic_data.destination, time_taken_secs, latest_timestamp from decentgrad$traffic_data_collection.traffic_data
    inner join (select origin, destination, max(ist_timestamp) latest_timestamp from decentgrad$traffic_data_collection.traffic_data
 	where origin='{origin}' and destination = '{destination}'
 	group by 1,2) last_timestamp
    on traffic_data.ist_timestamp=latest_timestamp
    and traffic_data.origin = last_timestamp.origin
    and traffic_data.destination = last_timestamp.destination
	where traffic_data.origin='{origin}' and traffic_data.destination = '{destination}') latest
 inner join (select origin, destination, avg(time_taken_secs) historical_average from decentgrad$traffic_data_collection.traffic_data
 	where origin='{origin}' and destination = '{destination}'
 	and TIMESTAMPDIFF(DAY, CURRENT_TIME(), ist_timestamp)<=30
 	group by 1,2
 	) historical
 	on latest.origin = historical.origin
 	and latest.destination = historical.destination
'''

def get_route_index(origin = 'KR Puram Metro Station', destination= 'Silk Board Junction', table_name='traffic_data', database='decentgrad$traffic_data_collection', user = 'decentgrad', password = database_password, host = 'decentgrad.mysql.pythonanywhere-services.com',port = '3306'):
    # Create a SQLAlchemy engine to connect to MySQL
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    query_text = query.format(**{"origin":origin,"destination":destination})
    print(query_text)
    with engine.connect() as connection:
        result = connection.execute(query_text)
    rows = result.fetchall()
    df = pd.DataFrame(rows)
    result = list(df.iloc[0])
    df.columns = ['Origin','Destination','latest_time','pct_change']
    index_dict = {
        'origin': result[0],
        'destination': result[1],
        'duration':result[2],
        'pct_change':result[3]
    }
    return index_dict

