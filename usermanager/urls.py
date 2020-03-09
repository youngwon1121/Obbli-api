from django.urls import path, include
from .views import UserViewSet, ResetPasswordViewSet, ResetPasswordViewSet, MyAnnounce, MyPageView, MyApplied, MyAnnounceDetail
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    #path('reset_password/', ResetPasswordViewSet.as_view(), name='reset-password'),
    path('me/', MyPageView.as_view()),
    path('me/announce/', MyAnnounce.as_view(), name='my-announce'),
    path('me/announce/<int:pk>/', MyAnnounceDetail.as_view(), name='my-announce-detail'),
    path('me/applying/', MyApplied.as_view(), name='my-applying'),
    path('', include(router.urls))
]

password_token = ResetPasswordViewSet.as_view({
    'post': 'token_create',
    'put' : 'token_update'
})

urlpatterns = format_suffix_patterns({
    path('password/token/', password_token, name='reset-password'),

})