"""
Authored by Andre Ferreira
W1772798
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Department


class LoginRequiredTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="sky1234")

    def test_department_list_redirects_if_not_logged_in(self):
        response = self.client.get(reverse("organisation:department_list"))
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_department_list_accessible_when_logged_in(self):
        self.client.login(username="testuser", password="sky1234")
        response = self.client.get(reverse("organisation:department_list"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_correct_credentials(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "sky1234"}
        )
        self.assertRedirects(response, reverse("organisation:department_list"))

    def test_login_with_wrong_password(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        # Matches django.contrib.auth.forms.AuthenticationForm.invalid_login
        self.assertContains(
            response,
            "Please enter a correct username and password",
        )

    def test_logout_redirects_to_login(self):
        self.client.login(username="testuser", password="sky1234")
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
