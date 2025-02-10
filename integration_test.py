from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from students.models import Student

class IntegrationTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123'
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

    def test_payment_integration(self):
        # Test the payment process (mocked)
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
        response = self.client.post(reverse('chapa_webhook'), {
            'status': 'success',
            'tx_ref': 'tx-ref-1'
        })
        self.assertEqual(response.status_code, 200)  # Should return success response
