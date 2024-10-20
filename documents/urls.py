from django.urls import path
from . import views

urlpatterns = [
    path('resumes/<int:resume_id>/documents/upload/', views.upload_document, name='upload_document'),
]
