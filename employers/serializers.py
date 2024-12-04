from rest_framework import serializers
from .models import EmployerProfile, Company

class EmployerProfileSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    verification_document = serializers.FileField(required=True)

    class Meta:
        model = EmployerProfile
        fields = ['company', 'verification_document']
        read_only_fields = ['is_verified']

    def create(self, validated_data):
        user = self.context['request'].user
        employer_profile = EmployerProfile.objects.create(user=user, **validated_data)
        return employer_profile

    def update(self, instance, validated_data):
        instance.company = validated_data.get('company', instance.company)
        instance.verification_document = validated_data.get('verification_document', instance.verification_document)
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)
        instance.save()
        return instance
