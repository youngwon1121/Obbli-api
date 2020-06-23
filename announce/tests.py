from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.status import *
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Announce(APITestCase):
    url = reverse('announce:announce-list')

    def setUp(self):
        self.user = User.objects.create_user(
            userid = 'peter9932',
            username = 'shinyoungwon',
            password = 'tls0dnjs',
            date_of_birth = '1998-11-21',
            phone = '01089619385',
            email = 'peter9932@naver.com'
        )

        self.token, _ = Token.objects.get_or_create(user=self.user)
    
    def test_get(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    
    def test_post_without_auth(self):
        res = self.client.post(self.url, {})
        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)

class Comment(APITestCase):
    url = reverse('announce:comment')

'''
TODO :: AnnounceSerializer TEST 구현
'''