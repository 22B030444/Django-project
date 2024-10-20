from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='profile')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='avatar', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name='birth date')
    number = models.CharField(max_length=20, null=True, blank=True, verbose_name='number')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)


    def __str__(self):
        return f'{self.user}'

