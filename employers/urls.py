from django.urls import path

from vacancies.views import JobApplicationStatusUpdateView
from .views import EmployerProfileView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/', EmployerProfileView.as_view(), name='employer-profile'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
