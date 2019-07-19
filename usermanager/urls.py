from django.urls import path
from .views import LogInView, JoinView, MyAnnounce, MyPageView, MyApplied, MyProfile, MyProfileDetail, MyAnnounceDetail, SendMailForPassword,ResetPassword
urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('join/', JoinView.as_view(), name='join'),
    path('reset_password/', ResetPassword.as_view(), name='reset-password'),
    path('reset_password/send_mail/', SendMailForPassword.as_view(), name='send-mail'),
    path('me/', MyPageView.as_view()),
    path('me/announce/', MyAnnounce.as_view(), name='my-announce'),
    path('me/announce/<int:pk>/', MyAnnounceDetail.as_view(), name='my-announce-detail'),
    path('me/profile/', MyProfile.as_view(), name='my-profile'),
    path('me/profile/<int:pk>/', MyProfileDetail.as_view(), name='my-profile-detail'),
    path('me/applying/', MyApplied.as_view(), name='my-applying'),
]