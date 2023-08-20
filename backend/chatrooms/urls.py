from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatRoomsList.as_view()),
    path("create", views.CreateChatRoom.as_view()),
]

websocket_patterms = [
    path("api/v1/chatrooms/<int:chatroom_pk>", views.ChatRoomsDetail.as_asgi()),
]
