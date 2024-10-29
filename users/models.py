from django.contrib.auth.models import User
from django.db import models

from resumes.models import Resume


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='profile')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='avatar', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name='birth date')
    number = models.CharField(max_length=20, null=True, blank=True, verbose_name='number')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)


    def __str__(self):
        return f'{self.user}'

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)  # Allow null values
    company_name = models.CharField(max_length=100)
    contact_email = models.EmailField()

    def __str__(self):
        return self.company_name

class ApprovedUser(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='approved_users')  # Связь с работодателем
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True)  # Дата одобрения

class EmployerFeedback(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return f'Feedback by {self.employer.company_name} on {self.resume.title}'