"""
Authored by Andre Ferreira
W1772798
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department, Team, Dependency


@login_required
def department_list(request):
    query = request.GET.get("q", "").strip()
    departments = Department.objects.prefetch_related("teams").all()
    if query:
        departments = departments.filter(name__icontains=query) | departments.filter(
            specialisation__icontains=query
        )
        departments = departments.distinct()
    return render(
        request,
        "organisation/department_list.html",
        {"departments": departments, "query": query},
    )


@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department.objects.prefetch_related("teams"), pk=pk)
    dependencies = Dependency.objects.select_related(
        "upstream_team", "downstream_team"
    ).filter(upstream_team__department=department)
    return render(
        request,
        "organisation/department_detail.html",
        {"department": department, "dependencies": dependencies},
    )


@login_required
def teams(request):
    query = request.GET.get("q", "").strip()
    team_list = (
        Team.objects.select_related("department")
        .prefetch_related(
            "downstream_dependencies__downstream_team",
            "upstream_dependencies__upstream_team",
        )
        .all()
    )
    if query:
        team_list = (
            team_list.filter(name__icontains=query)
            | team_list.filter(manager__icontains=query)
            | team_list.filter(skills__icontains=query)
            | team_list.filter(department__name__icontains=query)
        )
        team_list = team_list.distinct()
    return render(
        request,
        "organisation/teams.html",
        {"teams": team_list, "query": query},
    )
