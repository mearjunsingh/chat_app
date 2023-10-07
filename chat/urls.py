from django.urls import path

from .consumers import ChatConsumer
from .views import (
    home_page_view,
    chat_page_view,
)

urlpatterns = [
    path("", home_page_view, name="home_page_view"),
    path("chat/", chat_page_view, name="chat_page_view"),
]


websocket_urlpatterns = [
    path("ws/chat/<str:room_name>/<str:user>/", ChatConsumer.as_asgi()),
]
