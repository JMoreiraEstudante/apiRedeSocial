from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, UserDetail, UserList, followed, UserUpdate
app_name = 'user'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('followed/<int:pk>', followed, name="followed"),
    path('<int:pk>/edit', UserUpdate.as_view(), name="edit_user"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist'),
    path('<int:pk>', UserDetail.as_view(), name="user_detail"),
    path('', UserList.as_view(), name='userlist'),
]