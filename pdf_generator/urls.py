from django.urls import path
from .views import generate_pdf

urlpatterns = [
    path('resume/', lambda r: generate_pdf(r, 'resume_template.html'), name='generate_resume_pdf'),
    path('cover-letter/', lambda r: generate_pdf(r, 'cover_letter_template.html'), name='generate_cover_letter_pdf'),
    path('recommendation-letter/', lambda r: generate_pdf(r, 'recommendation_letter_template.html'), name='generate_recommendation_pdf'),
]
