from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from organisation.models import Department, Team


class ReportsViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="manager",
            password="testpass123",
        )
        self.department = Department.objects.create(
            name="Operations",
            leader="Sara",
            specialisation="Incident management",
        )
        Team.objects.create(
            name="Managed Team",
            manager="Mursal",
            department=self.department,
        )
        Team.objects.create(
            name="Unassigned Team",
            manager="",
            department=self.department,
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("reports:dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_shows_summary(self):
        self.client.login(username="manager", password="testpass123")
        response = self.client.get(reverse("reports:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Management Reports")
        self.assertContains(response, "Unassigned Team")

    def test_csv_export_downloads_data(self):
        self.client.login(username="manager", password="testpass123")
        response = self.client.get(reverse("reports:export_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("Total Teams,2", response.content.decode())
