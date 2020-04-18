from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from todo.tasks.models import Task
from todo.tasks.serializers import TaskSerializer, TaskListSerializer, TaskCreateSerializer


class TaskListView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "task_id"

    def get_queryset(self):
        return Task.objects.select_related("user").filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return TaskListSerializer
        elif  self.request.method.lower() == "post":
            return TaskCreateSerializer
        else:
            return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
