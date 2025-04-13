import os
import time

TOKEN = os.getenv("TOKEN")
YOUR_USER_ID = int(os.getenv("YOUR_USER_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")
POST_INTERVAL = int(os.getenv("POST_INTERVAL", 3600))
HASHTAG = '#ea7randompic'
# Временной интервал публикаций
START_TIME = dt_time(int(os.getenv("START_TIME")), 0)  
END_TIME = dt_time(int(os.getenv("END_TIME")), 0)    
