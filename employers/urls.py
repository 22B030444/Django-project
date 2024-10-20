from django.urls import path
from . import views

urlpatterns = [
    path('resumes/', views.employer_resume_list, name='employer_resume_list'),
    path('resumes/<int:resume_id>/feedback/', views.feedback_view, name='feedback_view'),
]
