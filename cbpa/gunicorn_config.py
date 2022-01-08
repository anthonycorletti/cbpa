"""gunicorn server configuration."""
import os

workers = 1
threads = 8
timeout = 0
bind = f":{os.environ.get('PORT', '8002')}"
worker_class = "uvicorn.workers.UvicornWorker"
