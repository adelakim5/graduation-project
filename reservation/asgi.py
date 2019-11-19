import os
import django
from channels.routing import get_default_application
# from some_asgi_library import AmazingMiddleware

# application = AmazingMiddleware(application)

# os.environ['DJANGO_SETTINGS_MODULE'] = 'reservation.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation.settings')
django.setup()

application = get_default_application()


