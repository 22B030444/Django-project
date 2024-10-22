from django.urls import path
from . import views
from .views import MainPage

urlpatterns = [
    path('resume/', MainPage.as_view(), name='main-page'),
    path('resume/create/', views.create_resume, name='create_resume'),
    path('generate/', views.generate_resume, name='generate_resume'),
    path('resume/<int:id>/edit/', views.edit_resume, name='edit_resume'),
    path('resume/<int:id>/', views.resume_detail, name='resume_detail'),
    path('resume/<int:id>/preview/', views.resume_preview, name='resume_preview'),
    path('resume/<int:id>/pdf/', views.resume_pdf_view, name='resume_pdf'),
    path('resume/github/add/', views.resume_add_project, name='resume_add_project'),
]