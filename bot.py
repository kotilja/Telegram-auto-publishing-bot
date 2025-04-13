import telebot
import threading
import queue
import time
from datetime import timedelta, datetime
from flask import Flask, request
from config import TOKEN, YOUR_USER_ID, CHANNEL_ID, POST_INTERVAL, HASHTAG, START_TIME, END_TIME
import os

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

media_queue = queue.Queue()

# Проверка времени публикации
def is_time_allowed():
    now = datetime.now().time()
    return START_TIME <= now < END_TIME

# Ожидание разрешенного времени
def wait_until_allowed():
    now = datetime.now()
    if now.time() >= END_TIME:
        tomorrow = datetime.combine(now.date(), START_TIME) + timedelta(days=1)
    else:
        tomorrow = datetime.combine(now.date(), START_TIME)

    seconds_to_wait = (tomorrow - now).total_seconds()
    minutes = int(seconds_to_wait // 60)
    wait_until = tomorrow.strftime('%H:%M')
    print(f"⏳ Ждём {minutes} минут до {wait_until}...")
    time.sleep(seconds_to_wait)

# Поток публикации медиа
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
                bot.send_video(CHANNEL_ID, file_id, caption=HASHTAG)
            print(f"✅ Опубликовано {file_type}")
        except Exception as e:
            print(f"❌ Ошибка при публикации: {e}")

        time.sleep(POST_INTERVAL)
        media_queue.task_done()

threading.Thread(target=publish_worker, daemon=True).start()

# Обработка вебхуков от Telegram
@app.route('/', methods=['POST'])
def webhook():
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(request.data.decode('utf-8'))])
    return "OK", 200

# Обработка медиа от доверенного пользователя
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

# Устанавливаем webhook при запуске сервера
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL"))
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
