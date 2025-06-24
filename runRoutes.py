import os, sys
import pandas as pd
from pytz import timezone
from datetime import datetime
import re
from append_to_sql_table import append_to_table
from download_mysql_table import download_table

ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')



print(ind_time)
filename = re.sub('\W+','',ind_time)  #filename for logs

project_home = '/home/decentgrad/traffic_alerts/'
os.chdir(project_home)

import json
#from dotenv import load_dotenv

from getduration import getDuration
from math import ceil

from dotenv import load_dotenv
import os

load_dotenv()

ola_api_key = os.getenv('ola_api_key')

#load_dotenv()

#api_key = os.environ['OLA_API_KEY']


routes = json.load(open('routes.json','r'))


routes_with_times=[]

for route in routes['routes']:
	#onward journey
    traffic_duration_results = getDuration(route['origin'],route['destination'], ola_api_key)
    traffic_duration_results['ist_timestamp'] = ind_time
    routes_with_times.append(traffic_duration_results)

    #return journey
    traffic_duration_results = getDuration(route['destination'], route['origin'], ola_api_key)
    traffic_duration_results['ist_timestamp'] = ind_time
    routes_with_times.append(traffic_duration_results)

df = pd.DataFrame(routes_with_times)
df.to_csv('logs/'+filename+'.csv', index=False) #save result to log file
append_to_table(df,'traffic_data')  #save results to a sql table

download_table() #save table to csv




