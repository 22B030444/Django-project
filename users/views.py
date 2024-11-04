# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, reverse, redirect, get_object_or_404
#
# from django.shortcuts import render
#
# # Create your views here.
#
# @login_required
# def login_view(request):
#     context = {}
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             next = request.POST.get('next')
#             if next:
#                 return redirect(next)
#             return redirect('index')
#         else:
#             context['error'] = True
#         return render(request, '#template-name')
#
# @login_required
# def logout_view(request):
#     logout(request)
#     next = request.GET.get('next')
#     if next:
#         return redirect(next)
#     return redirect('index')
#
from django.http import HttpResponseForbidden
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from resumes.models import Resume
from .form import UserLoginForm, ProfileForm, JobSeekerRegistrationForm, EmployerRegistrationForm
from .models import Profile, EmployerFeedback, ApprovedUser
from django.db import IntegrityError


def custom_csrf_failure_view(request, reason=""):
    template = loader.get_template('employer_page.html')  # replace with your template
    return HttpResponseForbidden(template.render())

class MainPage(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id if self.request.user.is_authenticated else None
        return context

def register(request):
    if request.method == "POST":
        if 'register_job_seeker' in request.POST:
            user_form = JobSeekerRegistrationForm(request.POST)
            if user_form.is_valid():
                user = user_form.save()
                Profile.objects.create(user=user)
                login(request, user)
                return redirect('main-page')  # Redirect job seeker

        elif 'register_employer' in request.POST:
            employer_form = EmployerRegistrationForm(request.POST)
            if employer_form.is_valid():
                employer = employer_form.save()
                login(request, employer.user)  # Ensure you link the employer to the user
                return redirect('employer-page')  # Redirect employer

    else:
        user_form = JobSeekerRegistrationForm()
        employer_form = EmployerRegistrationForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'employer_form': employer_form,
    })


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            email = user.email
            if '_' in email:
                return redirect('main-page')  # Redirect job seeker
            elif '.' in email:
                return redirect('employer-page')  # Redirect employer

        else:
            # Provide feedback for invalid credentials
            return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password.'})

    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {
        'user': request.user,
        'profile': profile
    })

# View for editing the profile
@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful edit
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})


def employer_dashboard(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.company_name:
        return HttpResponseForbidden("Access denied. Only employers can view this page.")

    employer = request.user.profile  # Accessing profile as an employer representation
    approved_users = ApprovedUser.objects.filter(employer=request.user).select_related('resume__user')
    resumes = Resume.objects.exclude(id__in=approved_users.values_list('resume_id', flat=True))

    context = {
        'company_name': employer.company_name,
        'approved_users': approved_users,
        'resumes': resumes,
    }

    return render(request, 'employer_page.html', context)

class EmployerPage(TemplateView):
    template_name = 'employer_page.html'  # Создайте шаблон для страницы работодателя

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id if self.request.user.is_authenticated else None
        # Здесь можно добавить дополнительные данные для страницы работодателя
        return context

@login_required
def approve_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    # Проверка, что работодатель имеет право одобрять это резюме
    if request.user.is_authenticated and hasattr(request.user, 'employer'):
        employer = request.user.employer
        # Проверяем, не одобрено ли уже это резюме
        if not ApprovedUser.objects.filter(employer=employer, resume=resume).exists():
            # Сохраните одобренное резюме
            approved_user = ApprovedUser(employer=employer, resume=resume)
            approved_user.save()

        return redirect('employer-page')  # Перенаправление обратно на панель управления

    return HttpResponseForbidden("У вас нет прав на одобрение этого резюме.")
def leave_feedback(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        feedback = EmployerFeedback.objects.create(
            employer=request.user.employer,  # Предполагается, что вы добавили связь с Employer в User
            resume=resume,
            feedback=feedback_text
        )
        return redirect('employer-page')

    return render(request, 'leave_feedback.html', {'resume': resume})