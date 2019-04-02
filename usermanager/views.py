from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from announce.models import Announce, Applying
from .serializers import ProfileSerializer, UserSerializer,  AnnounceDetailSerializer, MyAnnounceSerializer, MyAppliedSerializer
from .models import Profile
from .permissions import IsProfileOwner

User = get_user_model()

class LogInView(APIView):
    def post(self, request, *args, **kwargs):
        userid = request.data.get('userid')
        password = request.data.get('password')

        if userid is None or password is None:
            return Response({'error' : 'Didn\'t get either userid or password'})

        user = authenticate(userid=userid, password=password)
        if not user:
            return Response({'error' : 'Wrong userid or password'},
                status=status.HTTP_400_BAD_REQUEST
            )    
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token' : token.key},
            status=status.HTTP_201_CREATED
        )

class JoinView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class MyPageView(generics.RetrieveAPIView):
    '''
    View for /user/me/
    '''
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = User.objects.get(id=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

class MyAnnounce(generics.ListAPIView):
    '''
    View for /user/me/announce/
    '''
    serializer_class = MyAnnounceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Announce.objects.filter(writer=self.request.user)

class MyAnnounceDetail(generics.RetrieveAPIView):
    '''
    View for /user/me/announce/<pk>/
    '''
    serializer_class = AnnounceDetailSerializer
    def get_queryset(self):
        return Announce.objects.all()

class MyProfile(generics.ListCreateAPIView):
    '''
    View for /user/me/profile/
    '''
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    def get_queryset(self):
        owner = self.request.user
        return Profile.objects.filter(owner__userid=owner.userid)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MyProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    View for /user/me/profile/<pk>/
    '''
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsProfileOwner,)
    queryset = Profile.objects.all()

class MyApplied(generics.ListAPIView):
    '''
    View for /user/me/applying/
    '''
    serializer_class = MyAppliedSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Applying.objects.filter(applier=self.request.user)