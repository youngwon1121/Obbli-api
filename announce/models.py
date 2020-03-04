from django.contrib.auth import get_user_model
from board_api.models import DefaultModel
from usermanager.models import Profile
from instrument.models import Instrument
from django.db import models

User = get_user_model()

class Announce(DefaultModel):
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    writer = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL, related_name='announce')
    title = models.CharField(max_length=30)
    content = models.TextField()
    appointment_wage = models.IntegerField()
    appointment_location = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    deadline = models.DateTimeField()   #지원기한
    cutoff = models.DateTimeField()     #실마감날짜
    
    def __str__(self):
        return self.title

class Comment(DefaultModel):
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE, related_name='comments')
    writer = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL, related_name='my_comments')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies') #대댓글을 위해
    content = models.CharField(max_length=200)
    def __str__(self):
        return "{0}, {1}".format(self.pk, self.writer)


# Todo :: Applying을 어디에다가 둘지
class Applying(DefaultModel):
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE, related_name='applying')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='my_apply')
    applier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied')

    def __str__(self):
        return "{0}-{1}".format(self.profile.owner, self.announce.title)