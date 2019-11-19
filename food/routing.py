from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]

# from . import consumers
# from django.urls import re_path

# websocket_urlpatterns = [
#     re_path(r'ws/test/(?P<username>.*)/', consumers.UserTestConsumer),
# ]