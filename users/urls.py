from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    MainPage,
    approve_resume,
    leave_feedback,
    register,
    login_view,
    logout_view,
    profile_view,
    profile_edit,
    employer_dashboard,
    create_job_posting, reject_resume,
    job_search,
    apply_to_job
)

urlpatterns = [
    path('', MainPage.as_view(), name='base-page'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # Employer-related paths
    path('employer/', employer_dashboard, name='employer-page'),
    path('employer/approve/<int:resume_id>/', approve_resume, name='approve_resume'),
    path('employer/reject/<int:resume_id>/', reject_resume, name='reject_resume'),
    path('employer/create-job-posting/', create_job_posting, name='create_job_posting'),
    path('employer/leave-feedback/<int:resume_id>/', leave_feedback, name='leave_feedback'),

    # Authentication paths
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Profile paths
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),

    #Job seeker-related paths
    path('job-search/', job_search, name='job-search'),
    path('apply/<int:job_id>/', apply_to_job, name='apply-to-job'),
]
