from django.urls import path,include
from . import views
from .views import register_seeker,register_employer,admin_login,get_seekers,get_employers,approve_seeker,approve_employer,all_seekers,all_employers

urlpatterns = [
    path('api/register-seeker/', register_seeker, name='register_seeker'),
    path('api/register-employer/', register_employer, name='register-employer'),
    path('api/login/', admin_login, name='login'),
    path('api/get-seekers/', get_seekers, name='get_seekers'),
    path('api/get-employers/', get_employers, name='get_employers'),
    path('api/approve_seeker/', approve_seeker, name='approve_seeker'),
    path('api/approve-employer/', approve_employer, name='approve_employer'),
    path('api/all-seekers/', all_seekers, name='all_seekers'),
    path('api/all-employers/', all_employers, name='all_employers'),
    path('api/reject_seeker/', views.reject_seeker, name='reject_seeker'),
    path('api/reject_employer/', views.reject_employer, name='reject_employer'),
    path('api/remove_employer/', views.remove_employer, name='remove_employer'),
    path('api/remove_seeker/', views.remove_seeker, name='remove_seeker'),
    path('api/admin-details/', views.get_admin_details, name='admin-details'),
    path('api/update-admin/', views.update_admin_details, name='update-admin'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/token/', include('djoser.urls.authtoken')),
    path('api/reset-password/', views.reset_password, name='reset-password'),
    path('api/post-job/', views.post_job, name='post-job'),
    path('api/posted-jobs/', views.get_posted_jobs, name='get_posted_jobs'),
    path('api/posted-jobs/', views.get_posted_jobs, name='get_posted_jobs'),
    path('api/job-details/<int:job_id>/', views.get_job_details, name='get_job_details'),
    path('api/edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('api/delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('posted-jobs/', views.posted_jobs, name='posted-jobs'),
    path('api/job-approvals/', views.job_approvals, name='job-approvals'),
]
