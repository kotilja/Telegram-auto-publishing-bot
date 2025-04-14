from flask import Flask, request
import telebot
from config import TOKEN, YOUR_USER_ID
from tasks import publish_media

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(content_types=['photo', 'video'])
def handle_media(message):
    print("📥 Получено сообщение от пользователя")  # для дебага

    if message.from_user.id != YOUR_USER_ID:
        bot.reply_to(message, "🚫 Ты не в списке доверенных!")
        return

    if message.photo:
        file_id = message.photo[-1].file_id
        publish_media.delay(file_id, 'photo')
        bot.reply_to(message, "🖼 Фото в очереди на публикацию!")

    elif message.video:
        file_id = message.video.file_id
        publish_media.delay(file_id, 'video')
        bot.reply_to(message, "📹 Видео в очереди на публикацию!")

if __name__ == '__main__':
    import os
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL"))
    port = int(os.getenv('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
