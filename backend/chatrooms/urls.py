from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatRoomsList.as_view()),
    path("create", views.CreateChatRoom.as_view()),
]

websocket_patterms = []
