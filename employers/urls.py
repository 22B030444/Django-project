from django.urls import path
from .views import employer_register,employer_dashboard, approve_resume, leave_feedback, employer_login, employer_logout
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', employer_register, name='employer_register'),
    path('login/', employer_login, name='employer_login'),
    path('logout/', employer_logout, name='logout'),
    path('dashboard/', employer_dashboard, name='employer_dashboard'),
    path('approve_resume/<int:resume_id>/', approve_resume, name='approve_resume'),
    path('leave_feedback/<int:resume_id>/', leave_feedback, name='leave_feedback'),
]
