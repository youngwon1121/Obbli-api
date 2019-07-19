from django.db import models
from django.contrib.auth import get_user_model
from usermanager.models import Profile

User = get_user_model()

class DefaultModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Announce(DefaultModel):
    INSTRUMENTAL_TYPES = (
        ('Wind', '관악기'),
        ('String', '현악기'),
        ('Percussion', '타악기'),
        ('Keyboard', '건반악기'),
        ('Vocal', '성악'),
        ('ETC', '기타')
    )
    instrumental_type = models.CharField(max_length=10, choices=INSTRUMENTAL_TYPES)
    title = models.CharField(max_length=30)
    content = models.TextField()
    writer = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL, related_name='announce')
    pay = models.IntegerField()
    locations = models.CharField(max_length=100)
    deadline = models.DateField()
    def __str__(self):
        return self.title

class Comment(DefaultModel):
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE, related_name='comments')
    writer = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL, related_name='my_comments')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.CharField(max_length=200)
    def __str__(self):
        return "{0}, {1}".format(self.pk, self.writer)

class Applying(DefaultModel):
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE, related_name='applying')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='my_apply')
    applier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied')
    def __str__(self):
        return "{0}-{1}".format(self.profile.owner, self.announce.title)