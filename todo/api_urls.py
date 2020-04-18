from django.urls import include, path


urlpatterns = [
    path("users/", include("todo.users.urls")),
    path("tasks/", include("todo.tasks.urls"))
]
