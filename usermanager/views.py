import hashlib
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMessage
from django.db.models import Case, When, Subquery, Value, BooleanField
from rest_framework import status, generics, exceptions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from announce.models import Announce, Applying
from .serializers import ProfileSerializer, UserSerializer,  AnnounceDetailSerializer, MyAnnounceSerializer, MyAppliedSerializer, ResetPWSerializer
from .models import Profile, ResetPW
from .permissions import IsProfileOwner

User = get_user_model()

class LogInView(APIView):
    def post(self, request, *args, **kwargs):
        userid = request.data.get('userid')
        password = request.data.get('password')

        if userid is None or password is None:
            return Response({'error' : 'Didn\'t get either userid or password'},
                status=status.HTTP_400_BAD_REQUEST    
            )

        user = authenticate(userid=userid, password=password)
        if not user:
            return Response({'error' : 'Wrong userid or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token' : token.key},
            status=status.HTTP_201_CREATED
        )

class JoinView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ResetPassword(generics.UpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        email = self.request.data.get('email')
        hash_key = self.request.data.get('hash_key')

        if email is None or hash_key is None:
            raise exceptions.ParseError('Empty email or empty hash_key')
        
        try : 
            sub = ResetPW.objects.filter(
                email=email, 
                verified=1, 
                hash_key=hash_key).values('email')[0:1]
            obj = User.objects.get(email=Subquery(sub))
        except User.DoesNotExist as e:
            raise exceptions.AuthenticationFailed()
        
        return obj
    
    def get_serializer(self, *args, **kwargs):
        if 'password' in kwargs['data']:
            kwargs['data']['password'] = make_password(kwargs['data']['password'])

        kwargs['data']['email'] = args[0].email
        kwargs['data']['date_of_birth'] = args[0].date_of_birth
        kwargs['data']['username'] = args[0].username
        kwargs['data']['userid'] = args[0].userid
        kwargs['data']['phone'] = args[0].phone
        return super(ResetPassword, self).get_serializer(*args, **kwargs)

class SendMailForPassword(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = ResetPWSerializer

    def perform_create(self, serializer):
        get_object_or_404(User, email=self.request.data['email'])

        hash_val = hashlib.sha256((str(timezone.localtime().time())+self.request.data['email']).encode()).hexdigest()
        obj = serializer.save(hash_key=hash_val)
        email_result = EmailMessage('비밀번호 변경', obj.hash_key, to=[obj.email]).send()

        if email_result != 1:
            raise exceptions.APIException()

    def put(self, request, *args, **kwargs):
        hash_key = request.data.get('hash_key')
        email = request.data.get('email')

        if hash_key is None or email is None:
            raise exceptions.ParseError('empty either email or hash_key')

        sub = ResetPW.objects.filter(
            email=email,
            created_at__gte=timezone.localtime()+timedelta(minutes=-3)
        ).order_by('-created_at')
        updated_row = ResetPW.objects.filter(pk=Subquery(sub.values('id')[0:1])).update(
                verified = Case(
                    When(
                        hash_key = hash_key,
                        then = Value(True)
                    ),
                default = Value(False),
                output_field = BooleanField()
            )
        )

        if updated_row == 0:
            raise exceptions.NotFound('인증 요청시간이 지났거나 요청한 적이 없습니다.')

        if sub.values('verified')[0]['verified'] is False:
            raise exceptions.PermissionDenied('Wrong hash_key')

        return Response({"detail":"success"})
        
class MyPageView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = User.objects.get(id=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

class MyAnnounce(generics.ListAPIView):
    serializer_class = MyAnnounceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Announce.objects.filter(writer=self.request.user).order_by('-created_at')

class MyAnnounceDetail(generics.RetrieveAPIView):
    serializer_class = AnnounceDetailSerializer
    def get_queryset(self):
        return Announce.objects.all()

class MyProfile(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        owner = self.request.user
        return Profile.objects.filter(owner__userid=owner.userid)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MyProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsProfileOwner,)
    queryset = Profile.objects.all()

class MyApplied(generics.ListAPIView):
    serializer_class = MyAppliedSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Applying.objects.filter(applier=self.request.user).order_by('-created_at')