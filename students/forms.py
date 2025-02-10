from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student

class StudentRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(required=True)
    contact_info = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=True)
    emergency_contact = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'full_name', 'date_of_birth', 'contact_info', 'address', 'gender', 'emergency_contact']


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'date_of_birth', 'contact_info', 'address', 'gender', 'emergency_contact', 'profile_picture']
