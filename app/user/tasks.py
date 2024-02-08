from datetime import datetime

from celery import shared_task
from django.contrib.sessions.models import Session


@shared_task
def check_active_sessions():
    """Check active sessions."""
    active_sessions = Session.objects.all()
    if active_sessions.exists():
        print("There are active sessions.")
    else:
        print("There are no active sessions.")
