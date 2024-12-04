from django.db import models
from users.models import User
from django.utils.timezone import now
from company.models import Company

class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    created_at = models.DateField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vacancies")
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['created_at']

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_applications")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to='applications/resumes/', null=True, blank=True)
    recommendation_letter = models.FileField(upload_to='applications/recommendations/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Application from {self.user.username} for {self.vacancy.title}"