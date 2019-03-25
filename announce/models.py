from django.db import models
from django.contrib.auth import get_user_model
from usermanager.models import Profile

User = get_user_model()
class Announce(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='announce', null=True, blank=False)
    pay = models.IntegerField()
    locations = models.CharField(max_length=100)
    deadline = models.DateTimeField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

'''
    Announce의 레코드가 삭제되었을때 Applying의 annunce에서 삭제된데이터를 포린키로 받는 것들 삭제
'''
class Applying(models.Model):
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE, related_name='applying')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='my_apply')
    def __str__(self):
        return "{0} {1}".format(self.announce, self.profile)