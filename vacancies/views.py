import logging
from rest_framework import status
from .models import Vacancy
from rest_framework.response import Response
from .permissions import IsEmployer, IsHunter
from .pagination import VacancyPagination
from rest_framework.exceptions import PermissionDenied
from employers.models import EmployerProfile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .serializers import VacancySerializer,JobApplicationStatusSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import generics
from .models import JobApplication
from .serializers import JobApplicationSerializer
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from .models import Vacancy
from datetime import timedelta

logger = logging.getLogger('api_access')

def vacancies_analytics(request):
    return render(request, 'vacancies/analytics.html')

def vacancies_per_month_api(request):
    end_date = now()
    start_date = end_date - timedelta(days=180)

    vacancies = Vacancy.objects.filter(created_at__gte=start_date, created_at__lte=end_date)

    months = []
    vacancy_counts = []

    for i in range(6):
        month_start = start_date + timedelta(days=i * 30)
        month_end = month_start + timedelta(days=30)
        months.append(month_start.strftime('%b %Y'))
        count = vacancies.filter(created_at__gte=month_start, created_at__lte=month_end).count()
        vacancy_counts.append(count)

    data = {
        'months': months,
        'vacancy_counts': vacancy_counts
    }

    return JsonResponse(data)

class VacancyListView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    pagination_class = VacancyPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['title', 'company', 'created_at', 'posted_by', 'salary']
    search_fields = ['title']
    ordering_fields = ['created_at', 'salary']
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        vacancies = Vacancy.objects.all()
        logger.info(f"User {user.username} is accessing the Vacancy List view.")
        logger.warning(f"User {user.username}  have permission to access the Vacancy List.")
        return vacancies



class VacancyCreateView(generics.CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        user = self.request.user
        logger.info(f"User {user.username} is attempting to create a vacancy.")

        try:
            employer_profile = EmployerProfile.objects.get(user=user, is_verified=True)
        except EmployerProfile.DoesNotExist:
            logger.error(f"User {user.username} is not a verified employer.")
            raise PermissionDenied("You must be a verified employer to create a vacancy.")

        serializer.save(posted_by=user)
        logger.info(f"User {user.username} successfully created a vacancy.")


class VacancyDetailView(generics.RetrieveAPIView):
    queryset =Vacancy.objects.all()
    serializer_class = VacancySerializer


class VacancyUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAdminUser | IsEmployer]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.groups.filter(name='Admin').exists():
    #         return Vacancy.objects.all()
    #     # elif user.groups.filter(name='Employer').exists():
    #     #     return Vacancy.objects.filter(posted_by=user)
    #     else:
    #         raise PermissionDenied("You do not have permission to update vacancies.")

    def perform_update(self, serializer):
        user = self.request.user
        vacancy = self.get_object()
        if vacancy.posted_by != user and not user.groups.filter(name='Admin').exists():
            logger.warning(f"User {user.username} tried to update a vacancy they didn't post.")
            raise PermissionDenied("You cannot update a vacancy you did not create.")
        logger.info(f"User {user.username} is updating vacancy {vacancy.id}.")
        serializer.save()

class VacancyDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsEmployer]

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.groups.filter(name='Admin').exists():
    #         return Vacancy.objects.all()
    #     # elif user.groups.filter(name='Employer').exists():
    #     #     return Vacancy.objects.filter(posted_by=user)
    #     else:
    #         raise PermissionDenied("You do not have permission to delete vacancies.")

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.posted_by != user and not user.groups.filter(name='Admin').exists():
            logger.warning(f"User {user.username} tried to delete a vacancy they didn't post.")
            raise PermissionDenied("You cannot delete a vacancy you did not create.")
        logger.info(f"User {user.username} is deleting vacancy {instance.id}.")
        instance.delete()



class JobApplicationCreateView(generics.CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsHunter | IsAdminUser]

    # def get_queryset(self):
    #     user = self.request.user
    #     vacancy = self.request.data.get('vacancy')
    #     print(vacancy)
    #     print('some')
    #     return JobApplication.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        vacancy_id = self.kwargs.get('pk')
        print(f'Vacancy ID from URL: {vacancy_id}')
        logger.info(f"User {user.username} is applying for vacancy {vacancy_id}.")


        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            logger.error(f"Vacancy {vacancy_id} does not exist.")

            raise PermissionDenied("The vacancy does not exist.")

        if vacancy.posted_by == user:
            logger.warning(f"User {user.username} tried to apply for their own vacancy.")

            raise PermissionDenied("You cannot apply for your own vacancy.")

        serializer.save(user=user, vacancy=vacancy)
        logger.info(f"User {user.username} successfully applied for vacancy {vacancy.id}.")


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class UserJobApplicationListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)


class EmployerJobApplicationsListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.groups.filter(name='Employer').exists():
            raise PermissionDenied("You do not have permission to view applications.")

        posted_vacancies = Vacancy.objects.filter(posted_by=user)

        if not posted_vacancies.exists():
            raise PermissionDenied("No vacancies found for this employer.")

        return JobApplication.objects.filter(vacancy__in=posted_vacancies)

class JobApplicationStatusUpdateView(generics.RetrieveUpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationStatusSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def update(self, request, *args, **kwargs):
        job_application = self.get_object()
        user = request.user
        if job_application.vacancy.posted_by != user:
            logger.warning(f"User {user.username} tried to update a job application for a vacancy they didn't post.")

            raise PermissionDenied("You can only update applications for your own vacancies.")

        new_status = request.data.get('status')
        if new_status not in dict(JobApplication.STATUS_CHOICES):
            logger.error(f"User {user.username} provided an invalid status choice.")

            return Response({"detail": "Invalid status choice."}, status=status.HTTP_400_BAD_REQUEST)

        job_application.status = new_status
        job_application.save()
        logger.info(f"User {user.username} updated job application {job_application.id} to {new_status}.")

        return Response(JobApplicationStatusSerializer(job_application).data, status=status.HTTP_200_OK)
