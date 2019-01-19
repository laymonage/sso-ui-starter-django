"""SSO UI tests module."""
import json

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django_cas_ng.signals import cas_user_authenticated

from .models import ORG_CODE


class SSOUITest(TestCase):
    """Test SSO UI app."""
    ATTRIBUTES = {
        "nama": "Ice Bear",
        "peran_user": "mahasiswa",
        "npm": "1706123123",
        "kd_org": "01.00.12.01"
    }

    def setUp(self):
        """Setup test."""
        self.user = User.objects.create_superuser(
            username='username', password='password', email='username@test.com'
        )

    def test_home_url_exists(self):
        """Test if home url exists (response code 200)."""
        response = self.client.get(reverse('sso_ui:home'))
        self.assertEqual(response.status_code, 200)

    def test_login_url_exists(self):
        """Test if login url exists and redirects to CAS server (response code 302)."""
        response = self.client.get(reverse('sso_ui:login'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(settings.CAS_SERVER_URL))

    def test_logout_url_exists(self):
        """Test if logout url exists and redirects to CAS server (response code 302)."""
        response = self.client.get(reverse('sso_ui:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(settings.CAS_SERVER_URL))

    def test_profile_url_redirect_unauthenticated(self):
        """Test if profile url redirects an unauthenticated user."""
        response = self.client.get(reverse('sso_ui:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_can_save_attributes(self):
        """Test if Profile model can save the attributes from CAS."""
        cas_user_authenticated.send(
            sender=self,
            user=self.user,
            created=False,
            attributes=SSOUITest.ATTRIBUTES
        )
        self.assertJSONEqual(
            json.dumps({
                "nama": self.user.get_full_name(),
                "peran_user": self.user.profile.role,
                "npm": self.user.profile.npm,
                "kd_org": self.user.profile.org_code
            }),
            SSOUITest.ATTRIBUTES
        )
        self.assertJSONEqual(
            json.dumps({
                "faculty": self.user.profile.faculty,
                "study_program": self.user.profile.study_program,
                "educational_program": self.user.profile.educational_program
            }),
            ORG_CODE['id'][SSOUITest.ATTRIBUTES['kd_org']]
        )
        self.assertEqual(self.user.email, f"{self.user.username}@ui.ac.id")
        self.assertEqual(self.user.first_name, "Ice")
        self.assertEqual(self.user.last_name, "Bear")

    def test_profile_str(self):
        """Test string representation of Profile model."""
        self.assertEqual(str(self.user.profile), self.user.username)

    def test_profile_url_show_data_authenticated(self):
        """Test if profile url shows data in the page for an authenticated user."""
        cas_user_authenticated.send(
            sender=self,
            user=self.user,
            created=False,
            attributes=SSOUITest.ATTRIBUTES
        )
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('sso_ui:profile'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        attributes = [
            self.user.get_full_name(),
            self.user.username,
            self.user.email,
            self.user.profile.org_code,
            self.user.profile.role,
            self.user.profile.npm,
            self.user.profile.faculty,
            self.user.profile.study_program,
            self.user.profile.educational_program
        ]
        for attr in attributes:
            self.assertIn(attr, content)

    def test_admin_cant_change_profile(self):
        """Test if admin can't change profile model fields."""
        self.client.login(username='username', password='password')
        response = self.client.get(
            reverse(
                'admin:sso_ui_profile_change',
                kwargs={'object_id': self.user.profile.id}
            )
        )
        content = response.content.decode('utf-8')
        self.assertNotIn('<input type="text"', content)
        self.assertIn('<div class="readonly">', content)
