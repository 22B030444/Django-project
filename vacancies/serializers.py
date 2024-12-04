from rest_framework import serializers
from .models import Vacancy
from employers.models import EmployerProfile
from company.models import Company
from .models import JobApplication
class VacancySerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    posted_hr = serializers.ReadOnlyField(source='posted_by.username')
    application_count = serializers.IntegerField(source='applications.count', read_only=True)

    class Meta:
        model = Vacancy
        fields = ['id', 'title', 'description', 'company', 'company_name', 'created_at', 'posted_by', 'posted_hr', 'application_count', 'salary']
        read_only_fields = ['created_at', 'posted_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                employer_profile = EmployerProfile.objects.get(user=user, is_verified=True)
                self.fields['company'].queryset = Company.objects.filter(id=employer_profile.company_id)
            except EmployerProfile.DoesNotExist:
                self.fields['company'].queryset = Company.objects.none()
        else:
            self.fields['company'].queryset = Company.objects.none()


class JobApplicationSerializer(serializers.ModelSerializer):
    vacancy_title = serializers.CharField(source='vacancy.title', read_only=True)
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = JobApplication
        fields = ['id', 'user', 'user_name', 'vacancy', 'vacancy_title', 'resume', 'recommendation_letter', 'status']
        read_only_fields = ['user', 'vacancy', 'status']

class JobApplicationStatusSerializer(serializers.ModelSerializer):
    vacancy_title = serializers.CharField(source='vacancy.title', read_only=True)
    user_name = serializers.ReadOnlyField(source='user.username')
    # resume = serializers.CharField(source='resume.url', read_only=True)  # Direct field to resume URL
    # recommendation_letter = serializers.CharField(source='recommendation_letter.url', read_only=True)  # Direct field to recommendation URL

    class Meta:
        model = JobApplication
        fields = ['id', 'status', 'user_name', 'vacancy_title', 'resume', 'recommendation_letter']

    def validate_status(self, value):
        valid_statuses = dict(JobApplication.STATUS_CHOICES)
        if value not in valid_statuses:
            raise serializers.ValidationError("Invalid status choice.")
        return value