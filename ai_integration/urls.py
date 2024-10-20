from django.urls import path
from . import views

urlpatterns = [
    path('resumes/<int:resume_id>/cover-letter/', views.generate_cover_letter, name='generate_cover_letter'),
    path('resumes/<int:resume_id>/optimize/', views.optimize_resume, name='optimize_resume'),
]
