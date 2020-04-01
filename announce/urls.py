from django.urls import include, path
from .views import AnnounceViewSet, AnnounceList, AnnounceDetail, ApplyingAnnounce, CommentView, CommentDetail

user_list = AnnounceViewSet.as_view({'get' : 'list', 'post' : 'create'})

app_name = 'announce'
urlpatterns = [
    path('', user_list),
    #path('', AnnounceList.as_view(), name='announce-list'),
    path('<pk>/', AnnounceDetail.as_view(), name='announce-detail'),
    path('<pk>/comment/', CommentView.as_view(), name='comment'),
    path('comment/<pk>/', CommentDetail.as_view(), name='comment-detail'),
    path('<pk>/applying/', ApplyingAnnounce.as_view())
]