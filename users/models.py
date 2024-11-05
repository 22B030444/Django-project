from django.contrib.auth.models import User
from django.db import models
from resumes.models import Resume

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Profile')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Avatar', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name='Birth Date')
    number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone Number')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True, verbose_name='Resume')

    def __str__(self):
        return f'{self.user.username} Profile'

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer', verbose_name='User')
    company_name = models.CharField(max_length=100, verbose_name='Company Name')
    contact_email = models.EmailField(verbose_name='Contact Email')

    def __str__(self):
        return self.company_name

class ApprovedUser(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='approved_users', verbose_name='Employer')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Resume')
    approval_date = models.DateTimeField(auto_now_add=True, verbose_name='Approval Date')

    def __str__(self):
        return f'{self.resume} approved by {self.employer.company_name}'

class EmployerFeedback(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, verbose_name='Employer')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name='Resume')
    feedback = models.TextField(verbose_name='Feedback')

    def __str__(self):
        return f'Feedback by {self.employer.company_name} on {self.resume}'

class JobPosting(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('internship', 'Internship'),
    ]

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_postings', verbose_name='Employer')
    title = models.CharField(max_length=255, verbose_name='Job Title')
    description = models.TextField(verbose_name='Job Description')
    location = models.CharField(max_length=255, verbose_name='Job Location')
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Salary')
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPE_CHOICES, verbose_name='Employment Type')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    def __str__(self):
        return self.title
