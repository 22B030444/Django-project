from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.shortcuts import render

# Create your views here.

@login_required
def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next = request.POST.get('next')
            if next:
                return redirect(next)
            return redirect('index')
        else:
            context['error'] = True
        return render(request, '#template-name')

@login_required
def logout_view(request):
    logout(request)
    next = request.GET.get('next')
    if next:
        return redirect(next)
    return redirect('index')

