from django.urls import path
from .views import VacancyListView, VacancyCreateView, VacancyDetailView, VacancyUpdateView, VacancyDeleteView, JobApplicationCreateView
from .views import UserJobApplicationListView, EmployerJobApplicationsListView, JobApplicationStatusUpdateView

urlpatterns = [
    path('', VacancyListView.as_view(), name='vacancy_list'),
    path('<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail'),
    path('create/', VacancyCreateView.as_view(), name='vacancy_create'),
    path('<int:pk>/edit/', VacancyUpdateView.as_view(), name='vacancy_edit'),
    path('<int:pk>/delete/', VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('<int:pk>/apply/', JobApplicationCreateView.as_view(), name='apply_for_job'),
    path('my-applications/', UserJobApplicationListView.as_view(), name='user_job_applications'),
    path('my-vacancy-applications/', EmployerJobApplicationsListView.as_view(), name='employer_job_applications'),
    path('applications/<int:pk>/status/', JobApplicationStatusUpdateView.as_view(), name='update_application_status'),
]
