import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

database_password = os.getenv('database_password')

def download_table(table_name='traffic_data', database='decentgrad$traffic_data_collection',user = 'decentgrad', password = database_password, host = 'decentgrad.mysql.pythonanywhere-services.com',port = '3306'):
    # Create a SQLAlchemy engine to connect to MySQL
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    df = pd.read_sql_table(table_name, con=engine)
    # Optional: Save the DataFrame to a CSV file
    df.to_csv(f'table_download/{table_name}.csv', index=False)
    # Close the connection
    engine.dispose()


