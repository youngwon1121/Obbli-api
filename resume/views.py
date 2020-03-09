from django.shortcuts import render

# Create your views here.

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