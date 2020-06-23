urlpatterns = [
    path('me/profile/', MyProfile.as_view(), name='my-profile'),
    path('me/profile/<int:pk>/', MyProfileDetail.as_view(), name='my-profile-detail'),
]