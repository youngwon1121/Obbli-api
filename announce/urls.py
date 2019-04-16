from django.urls import include, path
from .views import AnnounceList, AnnounceDetail, ApplyingAnnounce, CommentView, CommentDetail
urlpatterns = [
    path('', AnnounceList.as_view()),
    path('<pk>/', AnnounceDetail.as_view()),
    path('<pk>/comment/', CommentView.as_view()),
    path('comment/<pk>/', CommentDetail.as_view()),
    path('<pk>/applying/', ApplyingAnnounce.as_view())
]