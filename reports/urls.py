from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("download/csv/", views.export_csv, name="export_csv"),
    path("download/pdf/", views.export_pdf, name="export_pdf"),
]
