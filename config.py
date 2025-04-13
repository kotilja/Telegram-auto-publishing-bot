import os
from datetime import time as dt_time

TOKEN = os.getenv("TOKEN")
YOUR_USER_ID = int(os.getenv("YOUR_USER_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

POST_INTERVAL = int(os.getenv("POST_INTERVAL", 3600))
HASHTAG = os.getenv("HASHTAG", '#ea7randompic')

START_TIME = dt_time(int(os.getenv("START_TIME", 10)), 0)  # По умолчанию: 10:00
END_TIME = dt_time(int(os.getenv("END_TIME", 23)), 0)      # По умолчанию: 23:00
