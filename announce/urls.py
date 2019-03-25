from django.urls import include, path
from .views import AnnounceList, AnnounceDetail, ApplyingAnnounce
urlpatterns = [
    path('', AnnounceList.as_view()),
    path('<pk>/', AnnounceDetail.as_view()),
    path('<pk>/applying/', ApplyingAnnounce.as_view())
]