from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Student
import json

class IntegrationTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        # Create a corresponding Student instance
        Student.objects.create(
            user=self.user,
            full_name='Test User',
            date_of_birth='2000-01-01',
            contact_info='1234567890',
            address='Test Address',
            gender='M',
            emergency_contact='0987654321'
        )

    def test_student_registration_integration(self):
        # Test the full registration process
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
        self.assertTrue(Student.objects.filter(user=self.user).exists())

    def test_login_integration(self):
        # Test the login process
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)  # Should return the dashboard

    def test_end_to_end_registration_integration(self):
        # Test the full registration process including login and dashboard access
        response = self.client.post(reverse('register_student'), {
            'username': 'testuser5',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'full_name': 'Test User 5',
            'date_of_birth': '2000-01-01',
            'contact_info': '1234567890',
            'address': 'Test Address 5',
            'gender': 'M',
            'emergency_contact': '0987654321'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(get_user_model().objects.filter(username='testuser5').exists())

        # Log in the newly registered user
        self.client.login(username='testuser5', password='testpassword123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)  # Should return the dashboard

    def test_webhook_integration(self):

        # Test the payment process (mocked)
        self.client.login(username='testuser', password='testpassword123')  # Ensure user is logged in
        response = self.client.post(reverse('chapa_payment'), {
            'amount': 100,
            'email': self.user.email,
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 200)  # Should return payment page

    def test_dashboard_access_integration(self):
        # Test access to the student dashboard
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)  # Should return the dashboard

    def test_webhook_integration(self):
        # Test webhook handling (mocked)
        response = self.client.post(reverse('chapa_webhook'), json.dumps({
            'status': 'success',
            'tx_ref': 'tx-ref-1'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)  # Should return success response
