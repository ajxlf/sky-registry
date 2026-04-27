from django.db import models

from organisation.models import Team


class Meeting(models.Model):
    title = models.CharField(max_length=120)
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="meetings"
    )
    organiser_name = models.CharField(max_length=100)
    scheduled_for = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    agenda = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["scheduled_for", "id"]

    def __str__(self):
        return f"{self.title} ({self.scheduled_for:%Y-%m-%d %H:%M})"

