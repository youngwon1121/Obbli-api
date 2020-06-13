from django.urls import include, path
from rest_framework import routers
from .views import AnnounceViewSet, CommentViewSet, AnnounceDetail, ApplyingAnnounce, CommentView, CommentDetail

announce_list = AnnounceViewSet.as_view({'get' : 'list', 'post' : 'create'})
announce_detail = AnnounceViewSet.as_view({'get' : 'retrieve'})
comment_list = CommentViewSet.as_view({'get' : 'list', 'post' : 'create'})
comment_detail = CommentViewSet.as_view({'get' : 'retrieve'})

router = routers.SimpleRouter()
router.register(r'', AnnounceViewSet, basename='announce')

app_name = 'announce'
urlpatterns = router.urls
urlpatterns += [
    path('<announce_pk>/comments/', comment_list),
    path('<announce_pk>/comments/<pk>', comment_detail)
]


urlpatterns1 = [
    path('', announce_list),
    path('<pk>/', AnnounceDetail.as_view(), name='announce-detail'),
    path('<pk>/comments/', comment_list),
    #path('<pk>/comments/<pk>', comment_detail),
    #path('', AnnounceList.as_view(), name='announce-list'),
    path('<pk>/comment/', CommentView.as_view(), name='comment'),
    path('comment/<pk>/', CommentDetail.as_view(), name='comment-detail'),
    path('<pk>/applying/', ApplyingAnnounce.as_view())
]