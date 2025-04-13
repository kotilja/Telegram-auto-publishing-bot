import telebot
import threading
import queue
import time
from datetime import timedelta, datetime, time as dt_time
from config import TOKEN, YOUR_USER_ID, CHANNEL_ID, POST_INTERVAL, HASHTAG

bot = telebot.TeleBot(TOKEN)
media_queue = queue.Queue()

# Временной интервал публикаций
START_TIME = dt_time(8, 0)  # 8:00
END_TIME = dt_time(21, 0)    # 21:00

# Функция проверки времени (разрешено ли публиковать сейчас)
def is_time_allowed():
    now = datetime.now().time()
    if START_TIME <= now < END_TIME:
        return True
    return False

# Время ожидания до разрешённого интервала
def wait_until_allowed():
    now = datetime.now()
    if now.time() >= END_TIME:
        # Ждём до завтра до 10:00
        tomorrow = datetime.combine(now.date(), START_TIME) + timedelta(days=1)
    else:
        # Ждём сегодня до 10:00
        tomorrow = datetime.combine(now.date(), START_TIME)
    seconds_to_wait = (tomorrow - now).total_seconds()
    print(f"⏳ Ждём {int(seconds_to_wait // 60)} минут до 10:00...")
    time.sleep(seconds_to_wait)

# Функция публикации из очереди с учётом временных рамок
def publish_worker():
    while True:
        item = media_queue.get()
        file_id, file_type = item

        while not is_time_allowed():
            wait_until_allowed()

        try:
            if file_type == 'photo':
                bot.send_photo(CHANNEL_ID, file_id, caption=HASHTAG)
            elif file_type == 'video':
                bot.send_video(CHANNEL_ID, file_id, caption="#ea7webm")
            print(f"✅ Опубликовано {file_type}")
        except Exception as e:
            print(f"❌ Ошибка при публикации: {e}")

        time.sleep(POST_INTERVAL)
        media_queue.task_done()

threading.Thread(target=publish_worker, daemon=True).start()

@bot.message_handler(content_types=['photo', 'video'])
def handle_media(message):
    if message.from_user.id != YOUR_USER_ID:
        bot.reply_to(message, "🚫 Ты не в списке доверенных!")
        return

    if message.photo:
        file_id = message.photo[-1].file_id
        media_queue.put((file_id, 'photo'))
        bot.reply_to(message, "🖼 Фото добавлено в очередь!")

    if message.video:
        file_id = message.video.file_id
        media_queue.put((file_id, 'video'))
        bot.reply_to(message, "📹 Видео добавлено в очередь!")

bot.polling(none_stop=True)
