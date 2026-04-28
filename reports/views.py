import csv

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Value
from django.db.models.functions import Coalesce, Trim
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from organisation.models import Department, Team


def _report_data():
    user_model = get_user_model()
    total_teams = Team.objects.count()
    total_departments = Department.objects.count()
    total_users = user_model.objects.count()

    teams_without_managers = list(
        Team.objects.select_related("department")
        .annotate(manager_name=Trim(Coalesce("manager", Value(""))))
        .filter(manager_name="")
        .order_by("name")
    )

    departments_with_team_counts = list(
        Department.objects.annotate(team_count=Count("teams")).order_by("name")
    )

    return {
        "total_teams": total_teams,
        "total_departments": total_departments,
        "total_users": total_users,
        "teams_without_managers": teams_without_managers,
        "teams_without_managers_count": len(teams_without_managers),
        "departments_with_team_counts": departments_with_team_counts,
        "generated_at": timezone.localtime(),
    }


@login_required
def dashboard(request):
    context = _report_data()
    return render(request, "reports/dashboard.html", context)


@login_required
def export_csv(request):
    data = _report_data()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="sky_registry_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Sky Engineering Registry Report"])
    writer.writerow(["Generated", data["generated_at"].strftime("%Y-%m-%d %H:%M")])
    writer.writerow([])
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Total Teams", data["total_teams"]])
    writer.writerow(["Total Departments", data["total_departments"]])
    writer.writerow(["Total Users", data["total_users"]])
    writer.writerow(["Teams Without Managers", data["teams_without_managers_count"]])
    writer.writerow([])
    writer.writerow(["Department", "Number of Teams"])
    for department in data["departments_with_team_counts"]:
        writer.writerow([department.name, department.team_count])
    writer.writerow([])
    writer.writerow(["Teams Without Managers"])
    writer.writerow(["Team", "Department"])
    for team in data["teams_without_managers"]:
        writer.writerow([team.name, team.department.name])

    return response


@login_required
def export_pdf(request):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        messages.error(
            request,
            "PDF export requires reportlab. Run the install command and try again.",
        )
        return redirect("reports:dashboard")

    data = _report_data()
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="sky_registry_report.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)
    _, height = A4
    y = height - 50

    def write_line(text, size=11, gap=18):
        nonlocal y
        if y < 60:
            pdf.showPage()
            y = height - 50
        pdf.setFont("Helvetica", size)
        pdf.drawString(50, y, text)
        y -= gap

    write_line("Sky Engineering Registry Report", size=16, gap=26)
    write_line(f"Generated: {data['generated_at'].strftime('%Y-%m-%d %H:%M')}")
    write_line(f"Total Teams: {data['total_teams']}")
    write_line(f"Total Departments: {data['total_departments']}")
    write_line(f"Total Users: {data['total_users']}")
    write_line(
        f"Teams Without Managers: {data['teams_without_managers_count']}", gap=24
    )

    write_line("Department Summary", size=13, gap=22)
    for department in data["departments_with_team_counts"]:
        write_line(f"{department.name}: {department.team_count} team(s)")

    y -= 10
    write_line("Teams Without Managers", size=13, gap=22)
    if data["teams_without_managers"]:
        for team in data["teams_without_managers"]:
            write_line(f"{team.name} ({team.department.name})")
    else:
        write_line("All teams currently have managers assigned.")

    pdf.showPage()
    pdf.save()
    return response
