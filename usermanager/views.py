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
from .serializers import UserSerializer,  AnnounceDetailSerializer, MyAnnounceSerializer, MyAppliedSerializer, ResetPWSerializer
from .models import ResetPW
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
   
    @action(detail=False, methods=['PUT'])
    def password_update(self, request, *args, **kwargs):
        email = request.user.email
        password = request.data.get('password')

        if password is None:
            raise exceptions.ParseError('Empty password')

        verified = ResetPW.objects.filter(
                email=email
            ).values('verified')[0]

        if not verified:
            pass

        data = {
            'password' : make_password(password)
        }

        serializer = UserSerializer(request.user, data=data, fields=('password',))
        if serializer.is_valid():
            serializer.save()
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

class MyApplied(generics.ListAPIView):
    serializer_class = MyAppliedSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Applying.objects.filter(applier=self.request.user)\
            .select_related('profile', 'announce').order_by('-created_at')