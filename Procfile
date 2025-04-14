web: gunicorn bot:app
worker: celery -A tasks worker --loglevel=info
