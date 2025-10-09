"""
Celery worker for background tasks.

This worker processes:
- Audit event outbox
- Email notifications
- Data exports
- Scheduled cleanups
"""
import os
import sys

# Add parent directory to path to import from control-plane
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "control-plane"))

from celery import Celery
from celery.signals import worker_ready, worker_shutdown

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "control_plane.settings")

# Import Django to configure it
import django
django.setup()

# Create Celery app
app = Celery("worker")

# Load configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from installed apps
app.autodiscover_tasks()


@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    """Signal handler for when worker is ready."""
    print("Worker is ready and waiting for tasks...")


@worker_shutdown.connect
def on_worker_shutdown(sender, **kwargs):
    """Signal handler for when worker is shutting down."""
    print("Worker is shutting down...")


if __name__ == "__main__":
    app.start()
