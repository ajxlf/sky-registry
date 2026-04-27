from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from organisation.models import Team

from .forms import MeetingForm
from .models import Meeting


@login_required
def create(request):
    team_id = request.GET.get("team")
    initial = {}

    if team_id:
        team = Team.objects.filter(pk=team_id).first()
        if team:
            initial["team"] = team
            initial["title"] = f"{team.name} sync"
            initial["organiser_name"] = request.user.username or "admin"
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save()
            messages.success(request, f"Meeting '{meeting.title}' scheduled.")
            form = MeetingForm()
    else:
        form = MeetingForm(initial=initial)

    upcoming_meetings = Meeting.objects.select_related("team").order_by(
        "scheduled_for", "id"
    )[:10]

    return render(
        request,
        "schedule/create.html",
        {"form": form, "upcoming_meetings": upcoming_meetings},
    )

