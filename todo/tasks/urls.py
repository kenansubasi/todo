from django.urls import path

from todo.tasks.views import TaskListView

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list")
]
