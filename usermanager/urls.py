from django.urls import path
from .views import LogInView, ProfileView, JoinView, ProfileDetail
urlpatterns = [
    path('login/', LogInView.as_view()),
    path('join/', JoinView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile/<int:pk>/', ProfileDetail.as_view())
]