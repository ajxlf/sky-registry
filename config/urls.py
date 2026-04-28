from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("organisation.urls")),
    path("messages/", include("messaging.urls")),
    path("schedule/", include("schedule.urls")),
    path("reports/", include("reports.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
]
