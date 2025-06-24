import sys,os
from datetime import datetime
from pytz import timezone
from current_traffic_index import get_traffic_index
from get_specific_route_duration import get_route_index

sys.path.append(os.path.abspath(os.path.join(os.path.dirname('post_to_twitter.py'), '/home/decentgrad/', 'news_bot')))
from post_to_twitter import post_tweet

ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')

weekday = datetime.now(timezone("Asia/Kolkata")).strftime('%A')  # 'Friday'
hour = datetime.now(timezone("Asia/Kolkata")).strftime('%I').lstrip('0')  # '6' (removes leading zero)
am_pm =datetime.now(timezone("Asia/Kolkata")).strftime('%p')    # 'AM'


current_traffic_index = get_traffic_index()
percent_diff = int(100*current_traffic_index['traffic_index']-100)
percent_diff_time_of_day = int(100*current_traffic_index['traffic_index_given_time_of_day'] - 100)

if percent_diff>0:
    diff_adjective='🔺 more'
else:
    diff_adjective='⬇️ less'

if percent_diff_time_of_day>0:
    diff_adjective_time_of_day='🔺 more'
else:
    diff_adjective_time_of_day='⬇️ less'


tweet_content1 = "Current Traffic Status ("+datetime.now(timezone("Asia/Kolkata")).strftime('%d %b %Y %H:%M')+"):\n"+str(abs(percent_diff))+ "%"+diff_adjective+" compared to normal traffic\n"+str(abs(percent_diff_time_of_day))+ "%"+diff_adjective_time_of_day+" compared to normal traffic for "+weekday+" at "+str(hour)+am_pm+'\n'
post_tweet(tweet_content1)

############################################ route wise content ###########################################################
origin = 'KR Puram Metro Station'
destination = 'Silk Board Junction'

route_details = get_route_index(origin,destination)
duration_mins = int(route_details['duration']/60)
percent_diff = int(100*route_details['pct_change']-100)

if percent_diff>0:
    diff_adjective_time_of_day='🔺 more'
else:
    diff_adjective_time_of_day='⬇️ less'

tweet_content2 = origin+'-->'+destination+ ': '+str(duration_mins) +'mins. '+ str(percent_diff) + '%'+diff_adjective_time_of_day+' than normal.\n'
############################################ route wise content ###########################################################

origin = 'Silk Board Junction'
destination = 'KR Puram Metro Station'

route_details = get_route_index(origin,destination)
duration_mins = int(route_details['duration']/60)
percent_diff = int(100*route_details['pct_change']-100)

if percent_diff>0:
    diff_adjective_time_of_day='🔺 more'
else:
    diff_adjective_time_of_day='⬇️ less'

tweet_content3 = origin+'-->'+destination+ ': '+str(duration_mins) +'mins. '+ str(percent_diff) + '%'+diff_adjective_time_of_day+' than normal.\n'
############################################ route wise content ###########################################################



post_tweet("Traffic Status on ORR:\n"+tweet_content2+tweet_content3)
