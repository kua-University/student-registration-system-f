from django.urls import path
from . import views
from .views import login_user  # Import the login_user view


urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('logout/', views.logout_user, name='logout'),

    
    
    path('register/', views.register_student, name='register_student'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', login_user, name='login'),  # Add the login URL
    path('payment/', views.chapa_payment, name='chapa_payment'),

    path('payment/success/', views.payment_success, name='payment_success'),
    path('chapa-webhook/', views.chapa_webhook, name='chapa_webhook'),
]
