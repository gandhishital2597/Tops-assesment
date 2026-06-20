from django.test import TestCase
from django.urls import reverse
from .models import UserProfile
from .forms import UserProfileForm


class UserProfileModelTest(TestCase):
    def test_create_profile(self):
        profile = UserProfile.objects.create(username='alice', age=25, is_public=True)
        self.assertEqual(str(profile), 'alice')
        self.assertEqual(UserProfile.objects.count(), 1)


class UserProfileFormTest(TestCase):
    def test_age_under_13_is_rejected(self):
        form = UserProfileForm(data={'username': 'kid', 'age': 10, 'is_public': True, 'bio': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)

    def test_age_over_13_is_accepted(self):
        form = UserProfileForm(data={'username': 'teen', 'age': 14, 'is_public': True, 'bio': ''})
        self.assertTrue(form.is_valid())

    def test_blank_username_is_rejected(self):
        form = UserProfileForm(data={'username': '   ', 'age': 20, 'is_public': True, 'bio': ''})
        self.assertFalse(form.is_valid())


class ProfileViewTest(TestCase):
    def test_profile_list_view_status_code(self):
        response = self.client.get(reverse('profile_list'))
        self.assertEqual(response.status_code, 200)

    def test_profile_create_view_saves_to_db(self):
        response = self.client.post(reverse('profile_create'), {
            'username': 'bob', 'age': 30, 'is_public': True, 'bio': 'Hello world',
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertTrue(UserProfile.objects.filter(username='bob').exists())

    def test_export_csv_returns_csv_content_type(self):
        UserProfile.objects.create(username='carol', age=22, is_public=True)
        response = self.client.get(reverse('profile_export_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
