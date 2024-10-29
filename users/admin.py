from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ApprovedUser

admin.site.register(ApprovedUser)
