from django.contrib import admin

from .models import JobApplication, Vacancy

# Register your models here.

admin.site.register(JobApplication)
admin.site.register(Vacancy)
