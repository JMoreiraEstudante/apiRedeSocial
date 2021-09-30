from django.urls import path
from .views import PostList, PostDetail, liked

app_name = 'social'

urlpatterns = [
    path('<int:pk>', PostDetail.as_view(), name='postdetail'),
    path('', PostList.as_view(), name='postlist'),
    path('liked/<int:pk>', liked, name="edit_post"),
]
