from django.db import models
from resumes.models import Resume

class Employer(models.Model):
    company_name = models.CharField(max_length=100)
    contact_email = models.EmailField()

    def __str__(self):
        return self.company_name

class EmployerFeedback(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return f'Feedback by {self.employer.company_name} on {self.resume.title}'
