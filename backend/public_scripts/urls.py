from django.urls import path
from . import views

urlpatterns = [
    path("create", views.CreatePublicScript.as_view(), name="public-script-create"),
]
