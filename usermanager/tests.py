from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase
from rest_framework.status import *
from announce.views import AnnounceList
from rest_framework.authtoken.models import Token
from .models import Profile

User = get_user_model()
class TestSupport:
    @staticmethod
    def create_account():
        create_account = User.objects.create_user(
            userid = 'testest',
            password = 'pwtest',
            date_of_birth = '1998-11-21',
            username = 'shinyoungwon',
            phone = '01012345678',
            email = 'testest@naver.com'
        )
        return create_account
    
    @staticmethod
    def create_token():
        user = TestSupport.create_account()
        token = Token.objects.get_or_create(user=user)
        return user, token


class LoginViewTest(APITestCase):
    url = '/user/login/'
    def setUp(self):
        TestSupport.create_account()

    def test_authentication_with_valid_data(self):
        res = self.client.post(self.url, {
            "userid" : "testest",
            "password" : "pwtest"
        })
        self.assertEqual(201, res.status_code)

    def test_authentication_without_pw(self):
        res = self.client.post(self.url, {
            "userid" : "testest"
        })
        self.assertEqual(400, res.status_code)

    def test_authentication_with_wrong_pw(self):
        res = self.client.post(self.url, {
            "userid" : "testest",
            "password" : "tls0dnjs"
        })
        self.assertEqual(400, res.status_code)

class MyPageTest(APITestCase):
    url = '/user/me/'
    def setUp(self):
        TestSupport.create_token()

    def test_mypage_with_login(self):
        token = Token.objects.get(user__userid='testest')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        res = self.client.get(self.url)
        self.assertEqual(HTTP_200_OK, res.status_code)

    def test_mypage_without_login(self):
        res = self.client.get(self.url)
        self.assertEqual(HTTP_401_UNAUTHORIZED, res.status_code)

class MyAnnounceTest(APITestCase):
    url = reverse('my-announce')
    def setUp(self):
        TestSupport.create_token()

    def test_myannounce_with_login(self):
        token = Token.objects.get(user__userid='testest')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        res = self.client.get(self.url)
        self.assertEqual(HTTP_200_OK, res.status_code)
    
    def test_myannounce_without_login(self):
        res = self.client.get(self.url)
        self.assertEqual(HTTP_401_UNAUTHORIZED, res.status_code)

class MyProfileTest(APITestCase):
    url = reverse('my-profile')
    def setUp(self):
        TestSupport.create_token()
    
    def test_get_myprofile(self):
        token = Token.objects.get(user__userid='testest')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        res = self.client.get(self.url)
        self.assertEqual(HTTP_200_OK, res.status_code)

    def test_post_myprofile(self):
        token = Token.objects.get(user__userid='testest')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        res = self.client.post(self.url, {
            "intro" : "hihi"
        })
        self.assertEqual(HTTP_201_CREATED, res.status_code)

    def test_post_myprofile_without_data(self):
        token = Token.objects.get(user__userid='testest')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        res = self.client.post(self.url)
        self.assertEqual(HTTP_400_BAD_REQUEST, res.status_code)

class MyProfileDetailTest(APITestCase):
    def url(self, pk):
        return reverse('my-profile-detail', kwargs={"pk": pk})

    def setUp(self):
        user1, _ = TestSupport.create_token()
        self.profile = Profile.objects.create(intro="TESTESTPROFILEYO", owner=user1)
        
        user2 = User.objects.create_user(
            userid = 'testest2',
            password = 'pwtest2',
            date_of_birth = '1998-11-21',
            username = 'shinyoungwon',
            phone = '01012345678',
            email = 'testest2@naver.com'
        )
        token = Token.objects.get_or_create(user=user2)
    
    def test_get_myprofile_actually_not_mine(self):
        token = Token.objects.get(user__userid='testest2')
        self.client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
        res = self.client.get(self.url(self.profile.pk))
        self.assertEqual(HTTP_403_FORBIDDEN, res.status_code)