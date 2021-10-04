from django.urls import path
from .views import PostList, PostDetail, liked, PostUser, CommentList, commentLiked, PostFollowing

app_name = 'social'

urlpatterns = [
    path('<int:pk>', PostDetail.as_view(), name='postdetail'),
    path('following/<int:pk>', PostFollowing.as_view(), name='postfollowing'),
    path('', PostList.as_view(), name='postlist'),
    path('comment/<int:pk>', CommentList.as_view(), name='postlist'),
    path('liked/<int:pk>', liked, name="edit_post"),
    path('commentLiked/<int:pk>', commentLiked, name="edit_comment"),
    path('post/user/<int:pk>', PostUser.as_view(), name="post_user"),
]
