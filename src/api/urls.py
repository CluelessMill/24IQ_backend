from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views.auth_views import (
    SignInAPIView,
    SignUpAPIView,
    UpdateTokenAPIView,
    UserListDEBUG,
    LogOutAPIView
)
from .views.posts_views import PostAddAPIViews, PostCommentsAPIView, PostListAPIView
from .views.roles_views import (
    IsAdminAPIView,
    RoleListAPIView,
    RoleSetAPIView,
    RoleSetDEBUGAPIView,
)
from .views.user_views import ProfileAPIView

urlpatterns = [
    # * Post
    path("posts", PostListAPIView.as_view(), name="posts-list"),
    path("posts/create", PostAddAPIViews.as_view(), name="posts-create"),
    path("posts/comments", PostCommentsAPIView.as_view(), name="posts-comments"),
    # * Role
    path("role/is-admin", IsAdminAPIView.as_view(), name="is-admin"),
    path("role/list", RoleListAPIView.as_view(), name="role-list"),
    path("role/set", RoleSetAPIView.as_view(), name="role-set"),
    # * Auth
    path("auth/signup", SignUpAPIView.as_view(), name="sign-up"),
    path("auth/signin", SignInAPIView.as_view(), name="sign-in"),
    path("auth/refresh", UpdateTokenAPIView.as_view(), name="refresh-token"),
    path("auth/logout", LogOutAPIView.as_view(), name="logout"),
    # * User
    path("users/profile", ProfileAPIView.as_view(), name="profile"),
    # ! Debug
    path("role/set-deb", RoleSetDEBUGAPIView.as_view(), name="role-set-deb"),
    path("user/userlist-deb", UserListDEBUG.as_view(), name="user-list-deb"),
]

if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
