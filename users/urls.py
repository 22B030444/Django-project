from django.urls import path
from .views import MainPage, approve_resume, leave_feedback, register, login_view, logout_view, profile_view, \
    profile_edit, EmployerPage

urlpatterns = [
    path('', MainPage.as_view(), name='main-page'),  # Main page
    path('employer/', EmployerPage.as_view(), name='employer-page'),  # Employer dashboard
    path('register/', register, name='register'),  # Registration page
    path('login/', login_view, name='login'),  # Login page
    path('logout/', logout_view, name='logout'),  # Logout action
    path('profile/', profile_view, name='profile'),  # User profile page
    path('login/profile/edit/', profile_edit, name='profile_edit'),  # Edit profile page
    path('employer/<int:resume_id>/', approve_resume, name='approve_resume'),  # Approve resume
    path('employer/leave_feedback/<int:resume_id>/', leave_feedback, name='leave_feedback'),  # Leave feedback
]
