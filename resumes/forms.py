from django import forms
from .models import Resume, Project

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'summary', 'skills', 'experience', 'education', 'template']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_url']