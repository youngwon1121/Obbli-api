from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import ProfileSerializer, UserSerializer
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

class MyPageView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class ProfileView(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    #In get request
    def get_queryset(self):
        owner = self.request.user
        return Profile.objects.filter(owner__userid=owner.userid)

    #perform_create is used to save serializer in post request
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsProfileOwner,)
    queryset = Profile.objects.all()