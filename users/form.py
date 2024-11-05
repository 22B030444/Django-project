from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, JobPosting


class EmployerRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=100, required=True)
    contact_email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(EmployerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].label = "Company Name"
        self.fields['contact_email'].label = "Contact Email"


class JobSeekerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'number', 'resume']

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'description', 'location', 'salary', 'employment_type']  # Adjust fields as necessary

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }