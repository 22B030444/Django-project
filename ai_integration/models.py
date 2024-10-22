from django.db import models
from resumes.models import Resume

class CoverLetter(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    content = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)

class Optimization(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    suggestions = models.TextField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

class ChatSession(models.Model):
    user_input = models.TextField()
    bot_response = models.TextField()
    session_started = models.DateTimeField(auto_now_add=True)
