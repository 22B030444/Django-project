from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chatbot_interaction, name='chatbot_interaction'),
    path('generate_cover_letter/<int:resume_id>/', views.generate_cover_letter, name='generate_cover_letter'),
    path('optimize_resume/<int:resume_id>/', views.optimize_resume, name='optimize_resume'),
]
