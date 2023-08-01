"""
WSGI config for medication_scheduler project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from threading import Thread
from django.core.wsgi import get_wsgi_application
from health_service.utils import my_scheduled_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medication_scheduler.settings')
thread = Thread(target=my_scheduled_task)
thread.start()
application = get_wsgi_application()
