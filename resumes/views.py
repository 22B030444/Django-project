from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from .models import Resume, ResumeTemplate, ResumeDocument
from .forms import ResumeForm, ProjectForm

class MainPage(TemplateView):
    template_name = 'resume_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.user.id if self.request.user.is_authenticated else None
        return context
@login_required
def create_resume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('resume_detail', id=resume.id)
    else:
        form = ResumeForm()

    return render(request, 'create_resume.html', {'form': form})


@login_required
def edit_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('resume_detail', id=resume.id)
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'edit_resume.html', {'form': form})

def resume_detail(request, id):
    resume = get_object_or_404(Resume, id=id)
    return render(request, 'resume_detail.html', {'resume': resume})

def resume_preview(request, id):
    resume = get_object_or_404(Resume, id=id)
    return render(request, 'resume_preview.html', {'resume': resume})
def resume_pdf_view(request, id):
    document = get_object_or_404(ResumeDocument, resume__id=id)
    return FileResponse(document.pdf_file.open(), content_type='application/pdf')

@login_required
def resume_add_project(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.resume = resume
            project.save()
            return redirect('resume_detail', id=resume.id)
    else:
        form = ProjectForm()

    return render(request, 'add_project.html', {'form': form})

def generate_resume(request, pdfkit=None):
    # Здесь можно добавить логику для получения данных пользователя и резюме
    resume_data = {
        'name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        # добавьте сюда остальные данные для резюме
    }

    html = render_to_string('resume_pdf_template.html', resume_data)
    pdf = pdfkit.from_string(html, False)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response