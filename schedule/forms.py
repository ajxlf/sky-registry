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
            "title": forms.TextInput(
                attrs={"class": "form-input", "autocomplete": "off"}
            ),
            "team": forms.Select(attrs={"class": "form-input"}),
            "organiser_name": forms.TextInput(
                attrs={"class": "form-input", "autocomplete": "name"}
            ),
            "scheduled_for": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-input"}
            ),
            "duration_minutes": forms.NumberInput(
                attrs={"class": "form-input", "min": 1}
            ),
            "agenda": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-input",
                    "placeholder": "Optional agenda or notes",
                }
            ),
        }
