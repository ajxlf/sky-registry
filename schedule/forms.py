from django import forms

from .models import Meeting


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = [
            "title",
            "team",
            "organiser_name",
            "scheduled_for",
            "duration_minutes",
            "agenda",
        ]
        widgets = {
            "scheduled_for": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "agenda": forms.Textarea(attrs={"rows": 4}),
        }

