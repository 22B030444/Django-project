from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden
from django.template import loader
from django.contrib.auth.models import User
from .form import UserLoginForm, ProfileForm, JobSeekerRegistrationForm, EmployerRegistrationForm, JobPostingForm
from .models import Profile, EmployerFeedback, ApprovedUser, Employer
from resumes.models import Resume

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

def register(request):
    if request.method == "POST":
        if 'register_job_seeker' in request.POST:
            user_form = JobSeekerRegistrationForm(request.POST)
            if user_form.is_valid():
                user = user_form.save()
                Profile.objects.create(user=user)
                login(request, user)
                return redirect('main-page')

        elif 'register_employer' in request.POST:
            employer_form = EmployerRegistrationForm(request.POST)
            if employer_form.is_valid():
                user = employer_form.save()
                # Creating Employer instance linked to the new user
                Employer.objects.create(user=user, company_name=employer_form.cleaned_data['company_name'], contact_email=employer_form.cleaned_data['contact_email'])
                login(request, user)
                return redirect('employer-page')

    else:
        user_form = JobSeekerRegistrationForm()
        employer_form = EmployerRegistrationForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'employer_form': employer_form,
    })

# User login view
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            email = user.email

            # Redirect based on email format
            if '_' in email:
                return redirect('main-page')
            elif '.' in email:
                return redirect('employer-page')
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password.'})

    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

# User logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('base-page')

# Profile view
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {
        'user': request.user,
        'profile': profile
    })

# Profile editing view
@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})

# Employer dashboard view
@login_required
def employer_dashboard(request):
    if not hasattr(request.user, 'employer'):
        return HttpResponseForbidden("Access denied. Only employers can view this page.")

    employer = request.user.employer
    approved_users = ApprovedUser.objects.filter(employer=employer).select_related('resume__user')

    # Filter resumes based on criteria
    filter_param = request.GET.get('filter', 'all')
    if filter_param == 'pending':
        resumes = Resume.objects.exclude(id__in=approved_users.values_list('resume_id', flat=True))
    else:
        resumes = Resume.objects.all()

    context = {
        'company_name': employer.company_name,
        'approved_users': approved_users,
        'resumes': resumes,
        'filter_param': filter_param
    }
    return render(request, 'employer_page.html', context)

# Approve resume view
@login_required
def approve_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    if hasattr(request.user, 'employer'):
        employer = request.user.employer
        if not ApprovedUser.objects.filter(employer=employer, resume=resume).exists():
            ApprovedUser.objects.create(employer=employer, resume=resume)
        return redirect('employer-page')

    return HttpResponseForbidden("You do not have permission to approve this resume.")

@login_required
def reject_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    if hasattr(request.user, 'employer'):
        employer = request.user.employer
        # Check if the resume is approved and remove it if so
        approved_user = ApprovedUser.objects.filter(employer=employer, resume=resume)
        if approved_user.exists():
            approved_user.delete()  # Delete the approval entry if it exists

        return redirect('employer-page')  # Redirect to the employer's dashboard

    return HttpResponseForbidden("You do not have permission to reject this resume.")

# Leave feedback view
@login_required
def leave_feedback(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        EmployerFeedback.objects.create(
            employer=request.user.employer,
            resume=resume,
            feedback=feedback_text
        )
        return redirect('employer-page')

    return render(request, 'leave_feedback.html', {'resume': resume})

# Job posting view
@login_required
def create_job_posting(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_posting = form.save(commit=False)
            job_posting.employer = request.user.employer  # Associate job posting with the logged-in employer
            job_posting.save()
            return redirect('employer-page')  # Redirect after successful creation
    else:
        form = JobPostingForm()

    return render(request, 'create_job_posting.html', {'form': form})
