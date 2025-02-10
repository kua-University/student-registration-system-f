from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Student

class ComponentTestCase(TestCase):
    def test_user_creation(self):
        # Test user creation
        response = self.client.post(reverse('register_student'), {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'full_name': 'Test User',
            'date_of_birth': '2000-01-01',
            'contact_info': '1234567890',
            'address': 'Test Address',
            'gender': 'M',
            'emergency_contact': '0987654321'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

    def test_student_profile_creation(self):
        # Test student profile creation
        user = get_user_model().objects.create_user(username='testuser2', password='testpassword123')
        response = self.client.post(reverse('register_student'), {
            'username': 'testuser2',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'full_name': 'Test User 2',
            'date_of_birth': '2000-01-01',
            'contact_info': '1234567890',
            'address': 'Test Address 2',
            'gender': 'F',
            'emergency_contact': '0987654321'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(Student.objects.filter(user=user).exists())

    def test_form_validation(self):
        # Test form validation
        response = self.client.post(reverse('register_student'), {
            'username': '',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'full_name': 'Test User',
            'date_of_birth': '2000-01-01',
            'contact_info': '1234567890',
            'address': 'Test Address',
            'gender': 'M',
            'emergency_contact': '0987654321'
        })
        self.assertEqual(response.status_code, 200)  # Should return to the form with errors
