from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from students.models import Student

class SystemTesting(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.student = Student.objects.create(
            user=self.user,
            full_name='Test User',
            date_of_birth='2000-01-01',
            contact_info='1234567890',
            address='Test Address',
            gender='M',
            emergency_contact='0987654321'
        )

    def test_registration(self):
        response = self.client.post(reverse('register_student'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'full_name': 'New User',
            'date_of_birth': '2000-01-01',
            'contact_info': '1234567890',
            'address': 'New Address',
            'gender': 'F',
            'emergency_contact': '0987654321'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration

    def test_login(self):
        response = self.client.post(reverse('login'), {

            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_student_dashboard_access(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)  # Should return the dashboard

    def test_payment_page_access(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('chapa_payment'))
        self.assertEqual(response.status_code, 200)  # Should return the payment page
