from django.contrib import admin

from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("title", "team", "organiser_name", "scheduled_for", "duration_minutes")
    search_fields = ("title", "organiser_name", "team__name")
    list_filter = ("team",)

