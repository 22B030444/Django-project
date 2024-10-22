from django.contrib.admin import forms
from django import forms
from .models import Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['posted_date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'company' : forms.TextInput(attrs={'class': 'form-control', 'size':5}),
            'location' : forms.TextInput(attrs={'class': 'form-control', 'size':5}),
            # 'created_at': forms.DateField(),
        }



class VacancyForm2(forms.ModelForm):
    pass