from django.db import models
from django.contrib.auth import get_user_model
from board_api.models import DefaultModel
from instrument.models import Instrument
from resume.models import Resume

User = get_user_model()

class Announce(DefaultModel):
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT, related_name='announces')
    writer = models.ForeignKey(User, null=True, blank=False, on_delete=models.PROTECT, related_name='announces')
    title = models.CharField(max_length=30)
    content = models.TextField()
    appointment_wage = models.IntegerField()
    appointment_location = models.CharField(max_length=100)
    appointment_date = models.DateTimeField(blank=False, null=True)
    deadline = models.DateTimeField(blank=False, null=False)   #지원기한
    cutoff = models.DateTimeField(blank=False, null=True)     #실마감날짜
    
    def __str__(self):
        return self.title

class Comment(DefaultModel):
    announce = models.ForeignKey(Announce, on_delete=models.PROTECT, related_name='comments')
    writer = models.ForeignKey(User, null=True, blank=False, on_delete=models.PROTECT, related_name='comments')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT, related_name='replies') #대댓글을 위해
    content = models.CharField(max_length=200)
    def __str__(self):
        return "{0}, {1}".format(self.pk, self.writer)


# Todo :: Applying을 어디에다가 둘지
class Applying(DefaultModel):
    announce = models.ForeignKey(Announce, on_delete=models.PROTECT)
    resume = models.ForeignKey(Resume, on_delete=models.PROTECT)
    applier = models.ForeignKey(User, on_delete=models.PROTECT)