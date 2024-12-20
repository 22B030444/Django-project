"""
URL configuration for resume_builder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
schema_view = get_schema_view(
   openapi.Info(
      title="Vacancy Management API",
      default_version='v1',
      description="API for managing vacancies, applications, and user roles",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@vacancy.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('', RedirectView.as_view(url='/accounts/log/login', permanent=False)),
    path('resumes/', include('resumes.urls')),
    path('vacancy/', include('vacancies.urls')),
    path('company/', include('company.urls')),
    path('employer/', include('employers.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='swagger-schema'),
    path('pdf/', include('pdf_generator.urls')),
    # path('ai/', include('ai_integration.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
