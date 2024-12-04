import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from django.template import loader
from rest_framework.views import APIView

from employers.models import EmployerProfile
from .serializers import UserProfileUpdateSerializer
# from .form import UserLoginForm, ProfileForm, JobSeekerRegistrationForm, EmployerRegistrationForm, JobPostingForm, JobSearchForm,JobApplicationForm
# from .models import Profile
from resumes.models import Resume
from django.db.models import Q
from django.contrib.auth.models import Group, Permission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import User
from .serializers import UserRegisterSerializer

# Custom CSRF failure view

def custom_csrf_failure_view(request, reason=""):
    template = loader.get_template('employer_page.html')
    return HttpResponseForbidden(template.render())

# Main page view
class MainPage(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_id'] = self.request.user.id
        return context

# def register(request):
#     if request.method == "POST":
#         if 'register_job_seeker' in request.POST:
#             user_form = JobSeekerRegistrationForm(request.POST)
#             if user_form.is_valid():
#                 user = user_form.save()
#                 Profile.objects.create(user=user)
#                 login(request, user)
#                 return redirect('main-page')
#
#         elif 'register_employer' in request.POST:
#             employer_form = EmployerRegistrationForm(request.POST)
#             if employer_form.is_valid():
#                 user = employer_form.save()
#                 # Creating Employer instance linked to the new user
#                 # Employer.objects.create(user=user, company_name=employer_form.cleaned_data['company_name'], contact_email=employer_form.cleaned_data['contact_email'])
#                 login(request, user)
#                 return redirect('employer-page')
#
#     else:
#         user_form = JobSeekerRegistrationForm()
#         employer_form = EmployerRegistrationForm()
#
#     return render(request, 'register.html', {
#         'user_form': user_form,
#         'employer_form': employer_form,
#     })

# User login view
# def login_view(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             email = user.email
#
#             if '_' in email:
#                 return redirect('main-page')
#             elif '.' in email:
#                 return redirect('profile')
#         else:
#             return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password.'})
#
#     else:
#         form = UserLoginForm()
#
#     return render(request, 'login.html', {'form': form})



# Profile view
# @login_required
# def profile_view(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     return render(request, 'profile.html', {
#         'user': request.user,
#         'profile': profile
#     })


# Profile editing view
# @login_required
# def profile_edit(request):
#     profile = request.user.profile
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=profile)
#
#     return render(request, 'profile_edit.html', {'form': form})

# Employer dashboard view
# @login_required
# views.py

# @login_required
# def employer_dashboard(request):
#     if not hasattr(request.user, 'employer'):
#         return HttpResponseForbidden("Access denied. Only employers can view this page.")
#
#     employer = request.user.employer
#     job_postings = employer.job_postings.prefetch_related('applications__applicant')
#     approved_users = ApprovedUser.objects.filter(employer=employer).select_related('resume__user')
#     filter_param = request.GET.get('filter', 'all')
#     if filter_param == 'pending':
#         resumes = Resume.objects.exclude(id__in=approved_users.values_list('resume_id', flat=True))
#     else:
#         resumes = Resume.objects.all()
#
#
#     context = {
#         'company_name': employer.company_name,
#         'job_postings': job_postings,
#         'approved_users': approved_users,
#         'resumes': resumes,
#         'filter_param': filter_param
#
#     }
#     return render(request, 'employer_page.html', context)

# Approve resume view
# @login_required
# def approve_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id)
#
#     if hasattr(request.user, 'employer'):
#         employer = request.user.employer
#         if not ApprovedUser.objects.filter(employer=employer, resume=resume).exists():
#             ApprovedUser.objects.create(employer=employer, resume=resume)
#         return redirect('employer-page')
#
#     return HttpResponseForbidden("You do not have permission to approve this resume.")

# @login_required
# def reject_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id)
#
#     if hasattr(request.user, 'employer'):
#         employer = request.user.employer
#         # Check if the resume is approved and remove it if so
#         approved_user = ApprovedUser.objects.filter(employer=employer, resume=resume)
#         if approved_user.exists():
#             approved_user.delete()  # Delete the approval entry if it exists
#
#         return redirect('employer-page')  # Redirect to the employer's dashboard
#
#     return HttpResponseForbidden("You do not have permission to reject this resume.")

# Leave feedback view
# @login_required
# def leave_feedback(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id)
#
#     if request.method == 'POST':
#         feedback_text = request.POST.get('feedback')
#         EmployerFeedback.objects.create(
#             employer=request.user.employer,
#             resume=resume,
#             feedback=feedback_text
#         )
#         return redirect('employer-page')
#
#     return render(request, 'leave_feedback.html', {'resume': resume})

# Job posting view
# @login_required
# def create_job_posting(request):
#     if request.method == 'POST':
#         form = JobPostingForm(request.POST)
#         if form.is_valid():
#             job_posting = form.save(commit=False)
#             job_posting.employer = request.user.employer  # Associate job posting with the logged-in employer
#             job_posting.save()
#             return redirect('employer-page')  # Redirect after successful creation
#     else:
#         form = JobPostingForm()
#
#     return render(request, 'create_job_posting.html', {'form': form})


# @login_required
# def job_search(request):
#     form = JobSearchForm(request.GET or None)
#     job_postings = JobPosting.objects.all()
#
#     if form.is_valid():
#         # Filtering by employment type
#         employment_type = form.cleaned_data.get('employment_type')
#         if employment_type:
#             job_postings = job_postings.filter(employment_type=employment_type)
#
#         # Filtering by profession
#         profession = form.cleaned_data.get('profession')
#         if profession:
#             job_postings = job_postings.filter(title__icontains=profession)
#
#         # Filtering by location
#         location = form.cleaned_data.get('location')
#         if location:
#             job_postings = job_postings.filter(location__icontains=location)
#
#         # Filtering by salary range
#         min_salary = form.cleaned_data.get('min_salary')
#         max_salary = form.cleaned_data.get('max_salary')
#         if min_salary is not None:
#             job_postings = job_postings.filter(salary__gte=min_salary)
#         if max_salary is not None:
#             job_postings = job_postings.filter(salary__lte=max_salary)
#
#     return render(request, 'job_search.html', {
#         'form': form,
#         'job_postings': job_postings,
#     })



# @login_required
# def apply_to_job(request, job_id):
#     job_posting = get_object_or_404(JobPosting, id=job_id)
#     user = request.user
#
#     # Проверяем, есть ли у пользователя резюме
#     try:
#         resume = Resume.objects.get(user=user)
#     except Resume.DoesNotExist:
#         # Если резюме нет, перенаправляем на страницу создания резюме
#         return redirect('create_resume')  # Замените 'create_resume' на ваш URL для создания резюме
#
#     # Если резюме есть, можно выполнить действия по подаче заявки на работу
#     # Здесь логика подачи заявки на работу, если нужно
#
#     return redirect('job-search')  # Перенаправление на страницу поиска вакансий

logger = logging.getLogger('api_access')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def about_user(request):
    user = request.user
    roles = [group.name for group in user.groups.all()]
    return Response({
        'id': user.id,
        'username':user.username,
        'email':user.email,
        'first_name':user.first_name,
        'last_name':user.last_name,
        'is_staff':user.is_staff,
        'role':roles
    })

class UserProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"})
        else:
            return Response(serializer.errors, status=400)



@login_required
def logout_view(request):
    logout(request)
    return redirect('base-page')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        role = request.data.get('role', 'Hunter')
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        if role == 'Employer':
            EmployerProfile.objects.create(user=user)
            permissions = Permission.objects.filter(codename__in=['add_vacancy', 'change_vacancy', 'delete_vacancy'])
            group.permissions.set(permissions)

        if role == 'Admin':
                all_permissions = Permission.objects.all()
                group.permissions.set(all_permissions)
                print(all_permissions)
                user.user_permissions.set(all_permissions)
                user.save()
        logger.info(f"User registered successfully with username: {user.username} and role: {role}")

        return Response({
            'message': 'User registered successfully.',
            'username': user.username,
            'role': role,
            'token': token.key,
        }, status=status.HTTP_201_CREATED)
    logger.error('User registration failed due to validation errors.')

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        logger.info(f"User profile update requested for user: {user.username}")

        roles = [group.name for group in user.groups.all()]
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': roles,
        })

    def put(self, request):
        user = request.user
        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            logger.info(f"User profile updated successfully for user: {user.username}")
            serializer.save()
            logger.error(f"User profile update failed for user: {user.username} - {serializer.errors}")
            return Response({"message": "Profile updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


