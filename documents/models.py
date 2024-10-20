from django.db import models
from resumes.models import Resume

class Document(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file.name}'
