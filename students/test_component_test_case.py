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

    def test_successful_student_registration(self):
        # Test successful registration of a student
        response = self.client.post(reverse('register_student'), {
            'username': 'uniqueuser',  # Ensure this username is unique
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
        self.assertTrue(get_user_model().objects.filter(username='uniqueuser').exists())

    def test_student_profile_retrieval(self):
        # Test retrieval of student profile after registration
        user = get_user_model().objects.create_user(username='testuser4', password='testpassword123')
        student = Student.objects.create(user=user, full_name='Test User 4', date_of_birth='2000-01-01',
                                          contact_info='1234567890', address='Test Address 4', gender='F',
                                          emergency_contact='0987654321')
        self.client.login(username='testuser4', password='testpassword123')
        response = self.client.get(reverse('profile'))  # Assuming 'profile' is the URL name for the profile view
        self.assertEqual(response.status_code, 200)  # Should return a successful response
        self.assertContains(response, 'Test User 4')  # Check if the profile name is in the response

    def test_duplicate_username_registration(self):
        # Test that duplicate usernames cannot be registered
        self.client.post(reverse('register_student'), {
            'username': 'duplicateuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'full_name': 'Duplicate User',
            'date_of_birth': '2000-01-01',
            'contact_info': '1234567890',
            'address': 'Test Address',
            'gender': 'M',
            'emergency_contact': '0987654321'
        })
        response = self.client.post(reverse('register_student'), {
            'username': 'duplicateuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'full_name': 'Duplicate User 2',
            'date_of_birth': '2000-01-01',
            'contact_info': '1234567890',
            'address': 'Test Address 2',
            'gender': 'F',
            'emergency_contact': '0987654321'
        })
        self.assertEqual(response.status_code, 200)  # Should return to the form with errors
        self.assertContains(response, 'A user with that username already exists.')

    def test_invalid_data_submission(self):
        # Test that invalid data cannot be submitted
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
        self.assertContains(response, 'This field is required.')
