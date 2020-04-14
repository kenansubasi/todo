from django.urls import include, path


urlpatterns = [
    path("users/", include("todo.users.urls")),
]
