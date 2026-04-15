# organisation/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import Department, Team, Dependency


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(
            name="xTVWeb",
            leader="Sebastian Holt",
            specialisation="Web platform engineering",
        )
        self.team = Team.objects.create(
            name="Code Warriors",
            manager="Olivia Carter",
            status="Active",
            department=self.dept,
        )
        self.dep = Dependency.objects.create(
            description="Requires API Avengers for gateway access", department=self.dept
        )

    def test_department_str(self):
        self.assertEqual(str(self.dept), "xTVWeb")

    def test_team_str(self):
        self.assertEqual(str(self.team), "Code Warriors (xTVWeb)")

    def test_team_belongs_to_department(self):
        self.assertEqual(self.team.department, self.dept)

    def test_dependency_belongs_to_department(self):
        self.assertEqual(self.dep.department, self.dept)


class DepartmentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.dept = Department.objects.create(
            name="Mobile",
            leader="Violet Ramsey",
            specialisation="Mobile application services",
        )

    def test_list_view_returns_200(self):
        response = self.client.get(reverse("organisation:department_list"))
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_department(self):
        response = self.client.get(reverse("organisation:department_list"))
        self.assertContains(response, "Mobile")

    def test_search_filters_results(self):
        response = self.client.get(
            reverse("organisation:department_list"), {"q": "Mobile"}
        )
        self.assertContains(response, "Mobile")

    def test_detail_view_returns_200(self):
        response = self.client.get(
            reverse("organisation:department_detail", args=[self.dept.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_404_on_missing(self):
        response = self.client.get(
            reverse("organisation:department_detail", args=[9999])
        )
        self.assertEqual(response.status_code, 404)
