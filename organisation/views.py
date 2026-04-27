from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department


@login_required
def department_list(request):
    query = request.GET.get("q", "").strip()

    departments = Department.objects.prefetch_related("teams", "dependencies").all()

    if query:
        departments = departments.filter(name__icontains=query) | departments.filter(
            specialisation__icontains=query
        )
        departments = departments.distinct()

    return render(
        request,
        "organisation/department_list.html",
        {
            "departments": departments,
            "query": query,
        },
    )


@login_required
def department_detail(request, pk):
    department = get_object_or_404(
        Department.objects.prefetch_related("teams", "dependencies"), pk=pk
    )

    return render(
        request, "organisation/department_detail.html", {"department": department}
    )


def teams(request):
    return render(request, "organisation/teams.html")