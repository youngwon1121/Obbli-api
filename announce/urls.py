from django.urls import include, path
from .views import AnnounceList, AnnounceDetail, ApplyingAnnounce, CommentView, CommentDetail
app_name = 'announce'
urlpatterns = [
    path('', AnnounceList.as_view(), name='announce-list'),
    path('<pk>/', AnnounceDetail.as_view(), name='announce-detail'),
    path('<pk>/comment/', CommentView.as_view()),
    path('comment/<pk>/', CommentDetail.as_view()),
    path('<pk>/applying/', ApplyingAnnounce.as_view())
]