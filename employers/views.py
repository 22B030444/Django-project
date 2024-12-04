from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from vacancies.permissions import IsEmployer
from .models import EmployerProfile
from .serializers import EmployerProfileSerializer
from rest_framework.response import Response
from rest_framework import status

class EmployerProfileView(generics.RetrieveUpdateAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    # def perform_update(self, serializer):
    #     super().perform_update(serializer)
    #     serializer.save()
    #     return Response({"message": "Employer profile updated successfully"})
    #
    # def put(self, request, *args, **kwargs):
    #     employer_profile = self.get_object()
    #     if 'documentation' in request.data:
    #         file = request.data['documentation']
    #     return super().put(request, *args, **kwargs)
    #
    # def get_success_url(self):
    #     return redirect('profile')
