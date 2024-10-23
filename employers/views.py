from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from resumes.models import Resume
from .models import EmployerFeedback,ApprovedUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .forms import EmployerRegisterForm
from django.http import HttpResponseForbidden


def employer_register(request):
    if request.method == 'POST':
        form = EmployerRegisterForm(request.POST)
        if form.is_valid():
            # Создание пользователя
            user = User.objects.create_user(
                username=form.cleaned_data['company_name'],  # Или используйте другое поле для username
                email=form.cleaned_data['contact_email'],
                password=form.cleaned_data['password']  # Получение пароля из формы
            )
            # Создание работодателя
            employer = form.save(commit=False)
            employer.user = user  # Привязка работодателя к созданному пользователю
            employer.save()

            # Вход для нового пользователя
            login(request, user)
            return redirect('employer_dashboard')  # Перенаправление на панель управления
    else:
        form = EmployerRegisterForm()

    return render(request, 'employer_register.html', {'form': form})
def employer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'employer'):
            login(request, user)
            return redirect('employer_dashboard')
        else:
            # Если аутентификация не удалась или пользователь не работодатель
            return HttpResponseForbidden("Неверные данные для входа или вы не являетесь работодателем.")
    return render(request, 'employer_login.html')

def employer_logout(request):
    logout(request)
    return redirect('login') 
@login_required
def employer_dashboard(request):
    employer = request.user.employer
    approved_users = employer.approved_users.all()

    context = {
        'company_name': employer.company_name,
        'approved_users': approved_users,
    }

    return render(request, 'employer_dashboard.html', context)


@login_required
def approve_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    # Проверка, что работодатель имеет право одобрять это резюме
    if request.user.is_authenticated and hasattr(request.user, 'employer'):
        # Сохраните одобренное резюме
        approved_user = ApprovedUser(employer=request.user.employer, resume=resume)
        approved_user.save()
        return redirect('employer_dashboard')  # Перенаправление обратно на панель управления

    return HttpResponseForbidden("У вас нет прав на одобрение этого резюме.")
@login_required
def leave_feedback(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        feedback = EmployerFeedback.objects.create(
            employer=request.user.employer,  # Предполагается, что вы добавили связь с Employer в User
            resume=resume,
            feedback=feedback_text
        )
        return redirect('employer_dashboard')

    return render(request, 'leave_feedback.html', {'resume': resume})
