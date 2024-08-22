# routing.py

from django.urls import re_path
from ADSapp import consumers

websocket_urlpatterns = [
    re_path(r'ws/terminal/$', consumers.TerminalConsumer.as_asgi()),
]
