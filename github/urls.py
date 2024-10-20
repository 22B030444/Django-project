from django.urls import path
from . import views

urlpatterns = [
    path('link/', views.link_github, name='link_github'),
    path('projects/', views.fetch_github_projects, name='github_projects'),
    path('projects/add/<int:project_id>/', views.add_project_to_resume, name='add_project'),
]
