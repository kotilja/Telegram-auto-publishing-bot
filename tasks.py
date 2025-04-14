@celery.task
def publish_media(file_id, file_type):
    print(f"📤 Начинаем публикацию: {file_type}")
    
    if not is_time_allowed():
        print("⏱ Сейчас нельзя публиковать, ждём...")
        wait_until_allowed()

    try:
        if file_type == 'photo':
            bot.send_photo(CHANNEL_ID, file_id, caption=HASHTAG)
        elif file_type == 'video':
            bot.send_video(CHANNEL_ID, file_id, caption="#ea7webm")
        print(f"✅ Опубликовано: {file_type}")
    except Exception as e:
        print(f"❌ Ошибка при публикации: {e}")

    print(f"⏳ Пауза {POST_INTERVAL} сек до следующей публикации")
    time.sleep(POST_INTERVAL)
