from django.shortcuts import render

# Create your views here.

departments = [
    {
        "id": 1,
        "name": "Mobile Engineering",
        "leader": "Alex Smith",
        "specialisation": "Builds and maintains mobile applications across iOS and Android.",
        "teams": [
            {"name": "Mobile Player", "manager": "Priya Shah", "status": "Active"},
            {"name": "iOS Client", "manager": "Jordan Blake", "status": "Active"},
        ],
        "dependencies": [
            "Mobile Player → Backend APIs",
            "iOS Client → Mobile Player",
        ],
    },
    {
        "id": 2,
        "name": "Platform & Tools",
        "leader": "Morgan Reed",
        "specialisation": "Supports internal tooling, CI/CD, and developer workflows.",
        "teams": [
            {"name": "Build Systems", "manager": "Chris Young", "status": "Active"},
            {"name": "Developer Experience", "manager": "Nina Patel", "status": "Active"},
        ],
        "dependencies": [
            "Developer Experience → Build Systems",
        ],
    },
    {
        "id": 3,
        "name": "xTV Web",
        "leader": "Sam Carter",
        "specialisation": "Delivers web-based TV platform experiences and frontend systems.",
        "teams": [
            {"name": "Playback UI", "manager": "Leah James", "status": "Active"},
            {"name": "Web Platform", "manager": "Tom Fisher", "status": "Active"},
        ],
        "dependencies": [
            "Playback UI → Web Platform",
            "Web Platform → Backend APIs",
        ],
    },
]

def department_list(request):
    query = request.GET.get("q", "").strip().lower()

    if query:
        filtered_departments = [
            dept for dept in departments
            if query in dept["name"].lower() or query in dept["specialisation"].lower()
        ]
    else:
        filtered_departments = departments

    return render(request, "organisation/department_list.html", {
        "departments": filtered_departments,
        "query": request.GET.get("q", ""),
    })

def department_detail(request, pk):
    department = next((dept for dept in departments if dept["id"] == pk), None)

    return render(request, "organisation/department_detail.html", {
        "department": department
    })
