import json
from dotenv import load_dotenv
import os
from getduration import getDuration, getDurationGMaps_live
import time
import re
from append_to_sql_table import append_to_table
from pytz import timezone
from send_telegram_message import send_message
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

project_home = '/home/decentgrad/traffic_alerts/'
os.chdir(project_home)

ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')

print(ind_time)
filename = re.sub('\W+','',ind_time)+'-alerts'  #filename for logs


load_dotenv()
ola_api_key = os.getenv('ola_api_key')

alert_routes = json.load(open('alert_routes.json','r'))



while True:
    routes_with_times=[]
    ist_hour = datetime.now(ZoneInfo("Asia/Kolkata")).hour
    if 8 <= ist_hour <= 21:
        for route in alert_routes['routes']:
            traffic_duration_results = getDurationGMaps_live(route['origin'],route['destination'])
            duration_mins = int(traffic_duration_results['time_taken_secs']/60)
            speed = 3.6*(traffic_duration_results['distance']/traffic_duration_results['time_taken_secs'])
            traffic_duration_results_return = getDurationGMaps_live(route['destination'],route['origin'])
            speed_return = 3.6*(traffic_duration_results_return['distance']/traffic_duration_results_return['time_taken_secs'])
            duration_mins_return = int(traffic_duration_results_return['time_taken_secs']/60)
            if speed<5 or speed_return<5:
                send_message(route['name']+':🔴 Emergency: Up:'+str(round(speed))+', Down:'+str(round(speed_return))+' kmph')
            elif speed<7 or speed_return<7:
                send_message(route['name']+':🟠 Very Slow: Up:'+str(round(speed))+', Down:'+str(round(speed_return))+' kmph')
            elif speed<9 or speed_return<9:
                send_message(route['name']+':🟡 Slow: Up:'+str(round(speed))+', Down:'+str(round(speed_return))+' kmph')
            else:
                pass
            print(route['name']+': Up:'+str(round(speed))+', Down:'+str(round(speed_return))+' kmph')
            traffic_duration_results['ist_timestamp'] = ind_time
            traffic_duration_results_return['ist_timestamp'] = ind_time
            routes_with_times.append(traffic_duration_results)
            routes_with_times.append(traffic_duration_results_return)
            df = pd.DataFrame(routes_with_times)
            df.to_csv('logs/'+filename+'.csv', index=False) #save result to log file
            append_to_table(df,'traffic_data')  #save results to a sql table
    print("Waiting 5 minutes...")
    time.sleep(300)  # Wait 5 minutes
