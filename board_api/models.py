from django.db import models

'''
    blank, null의 dafault는 False
'''
class DefaultModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=False, null=True)

    class Meta:
        abstract = True