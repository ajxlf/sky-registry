from django.urls import path

from . import views

app_name = "schedule"

urlpatterns = [
    path("create/", views.create, name="create"),
]

