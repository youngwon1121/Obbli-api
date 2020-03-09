from django.db import models
from django.contrib.auth import get_user_model
from board_api.models import DefaultModel

# Create your models here.
User = get_user_model()

class ResumeBase(DefaultModel):
    intro = models.TextField()
    experience = models.TextField(blank=True)
    selfie = models.ImageField(default="me.jpg", blank=True, null=True)

    class Meta:
        abstract = True

class ResumeTemplate(ResumeBase):
    writer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ResumeTemplates')
    
    def __str__(self):
        return self.intro

class Resume(ResumeBase):
    writer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Resumes')
    template = models.ForeignKey(ResumeTemplate, on_delete=models.PROTECT, related_name='Resumes')