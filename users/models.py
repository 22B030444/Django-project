#models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from resumes.models import Resume
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Profile')
#     avatar = models.ImageField(upload_to='avatars/', verbose_name='Avatar', null=True, blank=True)
#     birth_date = models.DateField(null=True, blank=True, verbose_name='Birth Date')
#     number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone Number')
#     resume = models.FileField(upload_to='resumes/', null=True, blank=True, verbose_name='Resume')
#
#     def __str__(self):
#         return f'{self.user.username} Profile'

