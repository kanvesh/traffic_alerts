import pandas as pd
from sqlalchemy import create_engine

def append_to_table(df, table_name='traffic_data', database='decentgrad$traffic_data_collection',user = 'decentgrad', password = 'Rock$127',host = 'decentgrad.mysql.pythonanywhere-services.com',port = '3306'):
    # Create a SQLAlchemy engine to connect to MySQL
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    # Append the DataFrame to the MySQL table, use 'append' for adding data without overwriting
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    print('data appended succesfully')
    # Close the connection
    engine.dispose()
