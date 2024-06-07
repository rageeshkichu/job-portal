from django.urls import path
from .views import register_seeker,register_employer,admin_login,get_seekers,get_employers,approve_seeker,approve_employer

urlpatterns = [
    path('api/register-seeker/', register_seeker, name='register_seeker'),
    path('api/register-employer/', register_employer, name='register-employer'),
    path('api/login/', admin_login, name='login'),
    path('api/get-seekers/', get_seekers, name='get_seekers'),
    path('api/get-employers/', get_employers, name='get_employers'),
    path('api/approve_seeker/', approve_seeker, name='approve_seeker'),
    path('api/approve-employer/', approve_employer, name='approve_employer'),
]
