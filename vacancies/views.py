from django.apps import AppConfig
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .forms import VacancyForm
from .models import Vacancy
from django.contrib.auth.models import Group, Permission


# from django.contrib.auth.admin import

# Create your views here.



class VacancyListView(ListView):
    model = Vacancy
    form_class = VacancyForm
    template_name = ''
    context_object_name = 'vacancies'


class VacancyCreateView(CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = ''
    context_object_name = 'vacancies'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['employer'] = [self.request.user.pk]
        return initial

    def form_valid(self, form):
        vacancy = form.save(commit=False)
        vacancy.author = self.request.user
        print('form valid works')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('', kwargs={'pk': self.object.pk})


class VacancyDetailView(DetailView, CreateView):
    model = Vacancy
    template_name = ''
    form_class = VacancyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy = self.get_object()
        print(vacancy.managers.all())

        return context

    def get_success_url(self):
        return reverse('')

    def post(self, request, *args, **kwargs):
        vacancy = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form, vacancy)
        else:
            return self.form_invalid(form)



class VacancyUpdateView(UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = ''
    context_object_name = 'vacancies'

    def get_success_url(self):
        return reverse('')


# @login_required
class VacancyDeleteView(DeleteView):
    model = Vacancy
    template_name = ''
    context_object_name = 'vacancies'

    # success_url = reverse_lazy('project_list')

    # def dispatch(self, request, *args, **kwargs):
    #     # if not request.user.is_authenticated or not self.request.user.groups.filter(name='Manager').exists():
    #     return redirect('project_list')

    # def get(self, request, *args, **kwargs):
    #     return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('')
