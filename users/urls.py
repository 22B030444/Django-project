from django.urls import path
from .views import MainPage, approve_resume, leave_feedback, register, login_view, logout_view, profile_view, profile_edit, employer_dashboard

urlpatterns = [
    path('', MainPage.as_view(), name='main-page'),
    path('workseer/', MainPage.as_view(), name='main-page'),
    path('employer/', employer_dashboard, name='employer-page'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('login/profile/edit/', profile_edit, name='profile_edit'),
    path('employer/<int:resume_id>/', approve_resume, name='approve_resume'),
    path('employer/leave_feedback/<int:resume_id>/', leave_feedback, name='leave_feedback'),
]
