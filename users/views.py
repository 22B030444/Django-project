# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, reverse, redirect, get_object_or_404
#
# from django.shortcuts import render
#
# # Create your views here.
#
# @login_required
# def login_view(request):
#     context = {}
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             next = request.POST.get('next')
#             if next:
#                 return redirect(next)
#             return redirect('index')
#         else:
#             context['error'] = True
#         return render(request, '#template-name')
#
# @login_required
# def logout_view(request):
#     logout(request)
#     next = request.GET.get('next')
#     if next:
#         return redirect(next)
#     return redirect('index')
#
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


from .forms import UserRegisterForm, UserLoginForm, ProfileForm
from .models import Profile


class MainPage(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id if self.request.user.is_authenticated else None
        return context
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('main-page')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main-page')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('main-page')


def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {
        'user': request.user,
        'profile': profile
    })

# View for editing the profile
@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after successful edit
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})