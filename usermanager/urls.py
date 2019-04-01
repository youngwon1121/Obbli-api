from django.urls import path
from .views import LogInView, JoinView, MyAnnounce, MyPageView, MyApplied, MyProfile, MyProfileDetail, MyAnnounceDetail
urlpatterns = [
    path('login/', LogInView.as_view()),
    path('join/', JoinView.as_view()),
    path('me/', MyPageView.as_view()),
    path('me/announce/', MyAnnounce.as_view()),
    path('me/announce/<int:pk>/', MyAnnounceDetail.as_view()),
    path('me/profile/', MyProfile.as_view()),
    path('me/profile/<int:pk>/', MyProfileDetail.as_view()),
    path('me/applying/', MyApplied.as_view()),
]