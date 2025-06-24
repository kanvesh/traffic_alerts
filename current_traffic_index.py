import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

database_password = os.getenv('database_password')

query= '''with norms_by_route as (select origin,destination, (hour(ist_timestamp)) hr, avg(time_taken_secs) time_taken_historical from decentgrad$traffic_data_collection.traffic_data group by 1,2,3),
norms_by_time as (select origin,destination, weekday(ist_timestamp) wkday, hour(ist_timestamp) hr, avg(time_taken_secs) time_taken_historical_given_timeof_day from decentgrad$traffic_data_collection.traffic_data group by 1,2,3,4),
latst as (select origin,destination, min(weekday(ist_timestamp)) wkday, min(hour(ist_timestamp)) hr, avg(time_taken_secs) time_taken_latest from decentgrad$traffic_data_collection.traffic_data
            where TIMESTAMPDIFF(minute, ist_timestamp, CONVERT_TZ(NOW(), 'UTC', 'Asia/Kolkata'))<=30 group by 1,2),
 traffic_index_by_route_and_time as (
 select latst.origin, latst.destination, latst.wkday, latst.hr  time_taken_latest, time_taken_historical_given_timeof_day, 1.0*time_taken_latest/time_taken_historical_given_timeof_day traffic_index_given_time_of_day
 from latst inner join norms_by_time
 on latst.origin = norms_by_time.origin
 and latst.destination = norms_by_time.destination
 and latst.wkday = norms_by_time.wkday
 and latst.hr = norms_by_time.hr),
 traffic_index_by_route as (
 select latst.origin, latst.destination, avg(time_taken_historical) time_taken_historical, 1.0*avg(time_taken_latest)/avg(time_taken_historical) traffic_index
 from latst inner join norms_by_route
 on latst.origin = norms_by_route.origin
 and latst.destination = norms_by_route.destination
 and latst.wkday = norms_by_route.hr
 group by 1,2)
 select rt.origin, rt.destination, avg(traffic_index) traffic_index, avg(traffic_index_given_time_of_day) traffic_index_given_time_of_day from
 traffic_index_by_route r
 inner join traffic_index_by_route_and_time rt
 on r.origin = rt.origin
 and r.destination = rt.destination
 group by 1,2
'''

def get_traffic_index(table_name='traffic_data', database='decentgrad$traffic_data_collection', user = 'decentgrad', password = database_password, host = 'decentgrad.mysql.pythonanywhere-services.com',port = '3306'):
    # Create a SQLAlchemy engine to connect to MySQL
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    with engine.connect() as connection:
        result = connection.execute(query)
    rows = result.fetchall()
    df = pd.DataFrame(rows)
    df.columns = ['Origin','Destination','traffic_index','traffic_index_given_time_of_day']
    index_dict = {
        'traffic_index': round(np.mean(df.traffic_index),2),
        'traffic_index_given_time_of_day': round(np.mean(df.traffic_index_given_time_of_day),2),
        'full_data':df
    }
    return index_dict
