from django import forms
from .models import Employer

class EmployerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=128, required=True)

    class Meta:
        model = Employer
        fields = ['company_name', 'contact_email']  # Не забудьте добавить 'password'
