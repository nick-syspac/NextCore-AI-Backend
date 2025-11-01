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

# Add control-plane directory to path
# In Docker, it's mounted at /control-plane
# In local dev, it's in ../control-plane
control_plane_path = os.environ.get("CONTROL_PLANE_PATH", "/control-plane")
if not os.path.exists(control_plane_path):
    control_plane_path = os.path.join(os.path.dirname(__file__), "..", "control-plane")
sys.path.insert(0, control_plane_path)

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
