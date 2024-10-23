from resumes.models import Resume
from django.db import models
from django.contrib.auth.models import User

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
