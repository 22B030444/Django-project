from django.shortcuts import render, get_object_or_404
from .models import Employer, EmployerFeedback
from resumes.models import Resume

def employer_resume_list(request):
    resumes = Resume.objects.all()
    return render(request, 'employers/resume_list.html', {'resumes': resumes})

def feedback_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    feedbacks = EmployerFeedback.objects.filter(resume=resume)
    return render(request, 'employers/feedback.html', {'feedbacks': feedbacks, 'resume': resume})
