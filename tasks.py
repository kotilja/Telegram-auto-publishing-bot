import time
from datetime import datetime, timedelta
from config import TOKEN, CHANNEL_ID, POST_INTERVAL, HASHTAG, START_TIME, END_TIME, REDIS_BROKER
from celery import Celery
import telebot

bot = telebot.TeleBot(TOKEN)

celery = Celery('tasks', broker=REDIS_BROKER)

def is_time_allowed():
    now = datetime.now().time()
    return START_TIME <= now < END_TIME

def wait_until_allowed():
    now = datetime.now()
    if now.time() >= END_TIME:
        tomorrow = datetime.combine(now.date(), START_TIME) + timedelta(days=1)
    else:
        tomorrow = datetime.combine(now.date(), START_TIME)
    time.sleep((tomorrow - now).total_seconds())

@celery.task
def publish_media(file_id, file_type):
    if not is_time_allowed():
        wait_until_allowed()

    try:
        if file_type == 'photo':
            bot.send_photo(CHANNEL_ID, file_id, caption=HASHTAG)
        elif file_type == 'video':
            bot.send_video(CHANNEL_ID, file_id, caption=HASHTAG)
        print(f"✅ Опубликовано {file_type}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

    time.sleep(POST_INTERVAL)

