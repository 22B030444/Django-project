from django.contrib.auth.models import User
from django.db import models

class Vacancy(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name='Title')

    description = models.TextField(null=False, blank=False, verbose_name='Description')

    company = models.CharField(max_length=100, null=False, blank=False, verbose_name='Company')
    location = models.CharField(max_length=100, null=False, blank=False, verbose_name='Location')
    posted_date = models.DateField(null=False, blank=False, verbose_name='Posted Date')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Author')

    def __str__(self):
        return f'{self.title}'

# Create your models here.
