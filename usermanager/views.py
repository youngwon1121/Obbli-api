import hashlib
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMessage
from django.db.models import Case, When, Subquery, Value, BooleanField
from rest_framework import viewsets, mixins, status, generics, exceptions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from announce.models import Announce, Applying
from .serializers import ProfileSerializer, UserSerializer,  AnnounceDetailSerializer, MyAnnounceSerializer, MyAppliedSerializer, ResetPWSerializer
from .models import Profile, ResetPW
from .permissions import IsProfileOwner

User = get_user_model()

class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def login(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, fields=('userid', 'password'))
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(userid=serializer.validated_data['userid'], password=serializer.validated_data['password'])
        if not user:
            return Response({'error' : 'Wrong userid or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token' : token.key},
            status=status.HTTP_201_CREATED
        )

class ResetPasswordViewSet(viewsets.GenericViewSet):
    serializer_class = ResetPWSerializer

    @action(detail=False, methods=['POST'])
    def token_create(self, request, *args, **kwargs):
        email = request.user.email
        hash_key = hashlib.sha256((str(timezone.localtime().time())+request.user.email).encode()).hexdigest()
        serializer_data = {
            'email' : email,
            'hash_key' : hash_key
        }
        serializer = self.get_serializer(data = serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.save()

        email_result = EmailMessage('비밀번호 변경', serializer.hash_key, to=[serializer.email]).send()
        if email_result != 1:
            raise exceptions.APIException()

    @action(detail=False, methods=['PUT'])
    def token_update(self, request, *args, **kwargs):
        hash_key = request.data.get('hash_key')
        email = request.user.email

        if hash_key is  None:
            raise exceptions.ParseError('Empty email or empty hash_key')

        sub = ResetPW.objects.filter(
            email = email,
            hash_key = hash_key,
            created_at__gte=timezone.localtime()+timedelta(minutes=-3)
        ).order_by('-created_at').values('pk')[0:1]

        affected_row = ResetPW.objects.filter(pk = Subquery(sub)).update(
                verified = Case(
                    When(
                        hash_key = hash_key,
                        then = Value(True)
                    ),
                default = Value(False),
                output_field = BooleanField()
            )
        )

        if affected_row == 0:
            raise exceptions.NotFound('인증 요청시간이 지났거나 요청한 적이 없습니다.')

        return Response({"detail":"success"})
   
    #def change_password(self, request, *args, **kwargs):


#비밀번호 바꾸는 부분
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

    def get_object(self):
        try : 
            obj = Announce.objects.prefetch_related('applying__applier', 'applying__profile').get(pk=self.kwargs['pk'])
            return obj
        except Announce.DoesNotExist:
            raise exceptions.NotFound('Not exist page')

class MyProfile(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        owner = self.request.user
        return Profile.objects.prefetch_related('my_apply').filter(owner__userid=owner.userid)
    
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
        return Applying.objects.filter(applier=self.request.user)\
            .select_related('profile', 'announce').order_by('-created_at')