from django.shortcuts import render, get_object_or_404
from .models import Document
from resumes.models import Resume

def upload_document(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        file = request.FILES['document']
        Document.objects.create(resume=resume, file=file)
    return render(request, 'documents/upload_document.html', {'resume': resume})
