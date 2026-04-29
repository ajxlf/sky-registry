"""
Authored by Andre Ferreira
W1772798
"""

from django.urls import path, include
from . import views

app_name = "organisation"

urlpatterns = [
    path("", views.department_list, name="department_list"),
    path("department/<int:pk>/", views.department_detail, name="department_detail"),
    path("teams/", views.teams, name="teams"),
]
