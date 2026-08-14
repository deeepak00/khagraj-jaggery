"""
Gunicorn configuration for production deployment.
Referenced by the Procfile: `web: gunicorn -c gunicorn.conf.py app:app`
"""
import multiprocessing
import os

bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
workers = int(os.environ.get("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))
threads = int(os.environ.get("PYTHON_MAX_THREADS", 2))
worker_class = "sync"
timeout = int(os.environ.get("WEB_TIMEOUT", 60))
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info")
