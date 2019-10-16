from django.urls import path, include
from .views import UserViewSet, ResetPasswordViewSet, MyAnnounce, MyPageView, MyApplied, MyProfile, MyProfileDetail, MyAnnounceDetail, SendMailForPassword,ResetPassword
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'password', ResetPasswordViewSet, basename='password')

reset_token = ResetPasswordViewSet.as_view({
    'post': 'token_create'
})

urlpatterns = [
    #path('password/token/', reset_token, name='reset-password'),
    #path('reset_password/', ResetPassword.as_view(), name='reset-password'),
    #path('reset_password/send_mail/', SendMailForPassword.as_view(), name='send-mail'),
    path('me/', MyPageView.as_view()),
    path('me/announce/', MyAnnounce.as_view(), name='my-announce'),
    path('me/announce/<int:pk>/', MyAnnounceDetail.as_view(), name='my-announce-detail'),
    path('me/profile/', MyProfile.as_view(), name='my-profile'),
    path('me/profile/<int:pk>/', MyProfileDetail.as_view(), name='my-profile-detail'),
    path('me/applying/', MyApplied.as_view(), name='my-applying'),
]

urlpatterns = [
    path('', include(router.urls))
]