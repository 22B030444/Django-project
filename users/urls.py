from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import MainPage

urlpatterns = [
    path('', MainPage.as_view(), name='main-page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),  # Profile view
    path('login/profile/edit/', views.profile_edit, name='profile_edit'),  # Profile edit
]