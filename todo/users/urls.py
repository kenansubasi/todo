from django.urls import path

from todo.users.views import UserLoginView, UserLogoutView, UserDetailView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    path("<username>/", UserDetailView.as_view(), name="user-detail")
]
