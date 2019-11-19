"""
WSGI config for reservation project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation.settings')
os.environ["SECRET_KEY"] = "$&@n1s@u&&s($$us@=-snd(qpfw0!-@dhn&!@0&@-@0fnbd-!@"

application = get_wsgi_application()
