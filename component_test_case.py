from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from students.models import Student

class StudentRegistrationTest(TestCase):
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

class LoginAuthenticationTest(TestCase):
    def test_successful_login(self):
        # Test successful login
        self.client.post(reverse('register_student'), {
            'username': 'testuser3',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'full_name': 'Test User 3',
            'date_of_birth': '2000-01-01',
            'contact_info': '1234567890',
            'address': 'Test Address 3',
            'gender': 'M',
            'emergency_contact': '0987654321'
        })
        response = self.client.post(reverse('login_user'), {
            'username': 'testuser3',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_invalid_credentials(self):
        # Test invalid credentials
        response = self.client.post(reverse('login_user'), {
            'username': 'invaliduser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Should return to the login form with error

class DashboardAccessTest(TestCase):
    def test_student_dashboard_access(self):
        # Test student dashboard access with authentication
        self.client.post(reverse('register_student'), {
            'username': 'testuser4',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'full_name': 'Test User 4',
            'date_of_birth': '2000-01-01',
            'contact_info': '1234567890',
            'address': 'Test Address 4',
            'gender': 'M',
            'emergency_contact': '0987654321'
        })
        self.client.login(username='testuser4', password='testpassword123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)  # Should return the dashboard

    def test_unauthorized_access(self):
        # Test unauthorized access prevention
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

class PaymentIntegrationTest(TestCase):
    def test_payment_initialization(self):
        # Test payment initialization
        # Mock the payment API call here
        pass  # Implement mock payment test

    def test_webhook_handling(self):
        # Test webhook handling
        # Mock the webhook call here
        pass  # Implement mock webhook test
