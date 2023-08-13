from django.urls import path
from . import views

urlpatterns = [
    path("", views.SystemInfosList.as_view(), name="sysinfo-list"),
    path("create", views.CreateSystemInfo.as_view(), name="create-sysinfo"),
    path("<int:pk>", views.SystemInfoDetail.as_view(), name="detail"),
    path("refbook", views.RefBooksList.as_view(), name="refbook"),
    path("refbook/create", views.CreateRefBook.as_view(), name="create-refbook"),
    path("refbook/<int:pk>", views.RefBookDetail.as_view(), name="refbook-detail"),
    path("refdata", views.RefDatasList.as_view(), name="refdata"),
    path("refdata/create", views.CreateRefData.as_view(), name="create-refdata"),
    path("refdata/<int:pk>", views.RefDataDetail.as_view(), name="refdata-detail"),
]
