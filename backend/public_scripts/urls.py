from django.urls import path
from . import views

urlpatterns = [
    path("", views.PublicScriptList.as_view(), name="public-script"),
    path("create", views.CreatePublicScript.as_view(), name="public-script-create"),
]
