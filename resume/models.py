from django.db import models
from django.contrib.auth import get_user_model
from board_api.models import DefaultModel

# Create your models here.
User = get_user_model()

class ResumeBase(DefaultModel):
    title = models.TextField("제목")
    education = models.TextField("학력")
    experience = models.TextField("경력")
    selfie = models.ImageField("사진", default="me.jpg", blank=True, null=True)

    class Meta:
        abstract = True

class ResumeTemplate(ResumeBase):
    writer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ResumeTemplates')
    
    def __str__(self):
        return self.title

# 실제 제출되는 Resume
class Resume(ResumeBase):
    writer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Resumes')
    template = models.ForeignKey(ResumeTemplate, on_delete=models.PROTECT, related_name='Resumes')