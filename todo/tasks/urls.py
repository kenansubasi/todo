from django.urls import path

from todo.tasks.views import TaskListView, TaskDetailView

urlpatterns = [
    path("", TaskListView.as_view(), name="task-list"),
    path("<int:task_id>/", TaskDetailView.as_view(), name="task-detail")
]
