from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views.auth_views import (
    SignInAPIView,
    SignUpAPIView,
    UpdateTokenAPIView,
    UserListDEBUG,
    LogOutAPIView,
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
    path(route="posts", view=PostListAPIView.as_view(), name="posts-list"),
    path(route="posts/create", view=PostAddAPIViews.as_view(), name="posts-create"),
    path(route="posts/comments", view=PostCommentsAPIView.as_view(), name="posts-comments"),
    # * Role
    path(route="role/is-admin", view=IsAdminAPIView.as_view(), name="is-admin"),
    path(route="role/list", view=RoleListAPIView.as_view(), name="role-list"),
    path(route="role/set", view=RoleSetAPIView.as_view(), name="role-set"),
    # * Auth
    path(route="auth/signup", view=SignUpAPIView.as_view(), name="sign-up"),
    path(route="auth/signin", view=SignInAPIView.as_view(), name="sign-in"),
    path(route="auth/refresh", view=UpdateTokenAPIView.as_view(), name="refresh-token"),
    path(route="auth/logout", view=LogOutAPIView.as_view(), name="logout"),
    # * User
    path(route="users/profile", view=ProfileAPIView.as_view(), name="profile"),
    # ! Debug
    path(route="role/set-deb", view=RoleSetDEBUGAPIView.as_view(), name="role-set-deb"),
    path(route="user/userlist-deb", view=UserListDEBUG.as_view(), name="user-list-deb"),
]

if settings.DEBUG:
    urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
