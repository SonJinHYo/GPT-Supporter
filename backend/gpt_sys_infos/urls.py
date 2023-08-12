from django.urls import path
from . import views

urlpatterns = [
    path("create", views.CreateSysInfo.as_view(), name="create-sysinfo"),
    path("", views.SysInfosList.as_view(), name="sysinfo-list"),
]
