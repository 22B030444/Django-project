from django.shortcuts import render, get_object_or_404
from .models import CoverLetter, Optimization
from resumes.models import Resume

def generate_cover_letter(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    # AI logic for generating cover letter here
    cover_letter = CoverLetter.objects.create(resume=resume, content="AI-generated content")
    return render(request, 'ai_integration/cover_letter.html', {'cover_letter': cover_letter})

def optimize_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    # AI logic for analyzing resume
    optimization = Optimization.objects.create(resume=resume, suggestions="AI suggestions")
    return render(request, 'ai_integration/optimize_resume.html', {'optimization': optimization})
