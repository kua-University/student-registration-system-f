from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, StudentProfileForm
from .models import Student
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

def landing_page(request):
    return render(request, 'students/landing.html')

def chapa_payment(request):
    if request.method == 'POST':
        amount = 100  # Amount in ETB
        email = request.user.email  # User's email
        first_name = request.user.first_name  # User's first name
        last_name = request.user.last_name  # User's last name

        # Prepare Chapa payment data
        payload = {
            'amount': amount,
            'currency': 'ETB',
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'tx_ref': f'tx-ref-2{request.user.id}',  # Unique transaction reference
            'callback_url': settings.CHAPA_WEBHOOK_URL,
            'return_url': request.build_absolute_uri(reverse('payment_success')),  # Redirect after payment
        }

        # Make a request to Chapa API
        headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        response = requests.post(settings.CHAPA_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            # Redirect to Chapa payment page
            payment_url = response.json()['data']['checkout_url']
            return redirect(payment_url)
        else:
            return JsonResponse({'error': 'Payment initialization failed'}, status=400)

    return render(request, 'students/chapa_payment.html')

def payment_success(request):
    # Handle successful payment (e.g., update registration status)
    student = Student.objects.get(user=request.user)
    student.registration_status = True  # Update registration status to completed
    student.save()
    return render(request, 'students/payment_success.html')

@csrf_exempt
def chapa_webhook(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        # Verify the payment status
        if payload['status'] == 'success':
            tx_ref = payload['tx_ref']
            # Update the registration status or perform other actions
            print(f"Payment successful for transaction: {tx_ref}")
        return HttpResponse(status=200)
    return HttpResponse(status=400)

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()  # Save the user first
            # Create the Student object
            student = Student(
                user=user,
                full_name=form.cleaned_data['full_name'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                contact_info=form.cleaned_data['contact_info'],
                address=form.cleaned_data['address'],
                gender=form.cleaned_data['gender'],
                emergency_contact=form.cleaned_data['emergency_contact']
            )
            student.save()  # Save the Student object
            login(request, user)
            return redirect('student_dashboard')  # Redirect to dashboard after registration

    else:
        form = StudentRegistrationForm()
    return render(request, 'students/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_dashboard')  # Redirect to the dashboard after login
        else:
            return render(request, 'students/login.html', {'error': 'Invalid credentials'})
    return render(request, 'students/login.html')

@login_required
def home(request):
    return render(request, 'students/home.html')

@login_required
def profile(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'students/profile.html', {'student': student})

@login_required
def settings(request):
    return render(request, 'students/settings.html')

def logout_user(request):
    logout(request)
    return redirect('landing_page')

@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    return render(request, 'students/student_dashboard.html', {'student': student})


@login_required
def admin_dashboard(request):
    students = Student.objects.all()
    return render(request, 'students/admin_dashboard.html', {'students': students})
