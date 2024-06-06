from django.urls import path
from .views import register_seeker,register_employer,admin_login

urlpatterns = [
    path('api/register-seeker/', register_seeker, name='register_seeker'),
    path('api/register-employer/', register_employer, name='register-employer'),
    path('api/login/', admin_login, name='login'),
]
