web: gunicorn app.wsgi -b 0.0.0.0:$PORT --debug
worker: celery -A tasks worker --loglevel=info --concurrency=1