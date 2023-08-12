from django.urls import path
from . import views

urlpatterns = [
    path("", views.SysInfosList.as_view(), name="sysinfo-list"),
    path("create", views.CreateSysInfo.as_view(), name="create-sysinfo"),
    path("<int:pk>", views.SystemInfoDetail.as_view(), name="detail"),
]
