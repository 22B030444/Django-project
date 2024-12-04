from django.db import models
from django.contrib.auth.models import User
from company.models import Company

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employer_profile")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    verification_document = models.FileField(upload_to='verification_docs/')
    is_verified = models.BooleanField(default=False)
