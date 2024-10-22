from django.db import models
from django.contrib.auth.models import User

class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    template_file = models.FileField(upload_to='templates/')

    def _str_(self):
        return self.name


class Project(models.Model):
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)

    def _str_(self):
        return self.title


from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume')
    title = models.CharField(max_length=200, default='Untitled Resume')  # Default title
    summary = models.TextField(default='Summary not provided.')           # Default summary
    skills = models.TextField(default='No skills listed.')                # Default skills
    experience = models.TextField(default='No experience listed.')        # Default experience
    education = models.TextField(default='No education listed.')          # Default education
    created_at = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title  # Corrected __str__ method



class ResumeDocument(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='documents')
    pdf_file = models.FileField(upload_to='resume/')

    def _str_(self):
        return f"Resume PDF: {self.resume.title}"