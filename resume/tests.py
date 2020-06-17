from django.test import TestCase
from django.contrib.auth import get_user_model
from .serializers import ResumeTemplateSerializer
# Create your tests here.

User = get_user_model()

class ResumeTemplateSerializerTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(
            userid = 'peter9932',
            username = 'youngwon',
            phone = '01089619385',
            date_of_birth = '1998-11-21',
            email = 'youngwon1121'
        )

    def test_serializer(self):
        data = {
            'writer' : "1",
            'title' : '안녕하세요. 저는 신영원입니다',
            'education' : 'hello',
            'experience' : 'hello',
        }

        serializer = ResumeTemplateSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

        