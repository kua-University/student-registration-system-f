from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    contact_info = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    emergency_contact = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    student_id = models.CharField(max_length=10, unique=True, editable=False)
    registration_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = self.generate_student_id()
        super().save(*args, **kwargs)

    def generate_student_id(self):
        import random
        return f"STU{random.randint(1000, 9999)}"

    def __str__(self):
        return self.full_name