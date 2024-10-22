from django.urls import path
from .views import VacancyListView, VacancyCreateView, VacancyDetailView, VacancyUpdateView, VacancyDeleteView

urlpatterns = [
    path('', VacancyListView.as_view(), name='vacancy_list'),
    path('vacancy/<int:pk>/', VacancyDetailView.as_view(), name='vacancy_detail'),
    path('vacancy/new/', VacancyCreateView.as_view(), name='vacancy_create'),
    path('vacancy/<int:pk>/edit/', VacancyUpdateView.as_view(), name='vacancy_edit'),
    path('vacancy/<int:pk>/delete/', VacancyDeleteView.as_view(), name='vacancy_delete'),
]
