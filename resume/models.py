from django.db import models
from board_api import DefaultModel

# Create your models here.

class ResumeTemplate(DefaultModel):
    writer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='profiles')
    intro = models.TextField()
    experience = models.TextField(blank=True)
    selfie = models.ImageField(default="me.jpg", blank=True, null=True)

    def __str__(self):
        return self.intro

class Resume(ResumeTemplate):
    template = models.ForeignKey(ResumeTemplate, on_delete=models.PROTECT)