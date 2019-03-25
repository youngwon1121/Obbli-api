from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from usermanager.models import Profile
from .serializers import AnnounceSerializer, ApplyingSerializer
from .models import Announce, Applying
from .permissions import ReadForAnyAndWriteForAuthenticated, IsProfileOwner

User = get_user_model()

class AnnounceList(generics.ListCreateAPIView):
    serializer_class = AnnounceSerializer
    permission_classes = (ReadForAnyAndWriteForAuthenticated,)
    queryset = Announce.objects.all()

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

class AnnounceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnnounceSerializer
    queryset = Announce.objects.all()

'''
    announce : pk에서 얻음
    profile : json으로 전송 후 검증

    같은 Apply에 같은프로필로 중복지원 불가능
    프로필 json으로 받을때 해당 유저의 프로필 맞는지 permission확인
'''
class ApplyingAnnounce(generics.CreateAPIView):
    serializer_class = ApplyingSerializer
    queryset = Applying.objects.all()
    permission_classes = (IsAuthenticated, IsProfileOwner,)

    def perform_create(self, serializer):
        #print(self.request.__dict__)
        announce = get_object_or_404(Announce, pk=self.request.parser_context.get('kwargs').get('pk')) 
        serializer.save(announce=announce)