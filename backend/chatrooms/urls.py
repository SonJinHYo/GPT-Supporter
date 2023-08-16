from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatRoomsList.as_view()),
    path("create/<int:system_info_pk>", views.CreateChatRoom.as_view()),
]

websocket_patterms = [
    path("ws/chatroom/<int:pk>", views.ChatRoomsDetail.as_asgi()),
]
