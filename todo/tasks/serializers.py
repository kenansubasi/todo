from rest_framework import serializers

from todo.tasks.models import Task
from todo.users.serializers import UserRetrieveSerializer


class TaskSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ("id", "title", "is_completed", "user", "created_at", "updated_at")


class TaskListSerializer(TaskSerializer):
    pass


class TaskRetrieveSerializer(TaskSerializer):
    pass


class TaskCreateSerializer(TaskSerializer):

    class Meta:
        model = Task
        fields = ("id", "title", "is_completed", "user", "created_at", "updated_at")
        read_only_fields = ("is_completed", "user", "created_at", "updated_at")


class TaskUpdateSerializer(TaskSerializer):

    class Meta:
        model = Task
        fields = ("id", "title", "is_completed")
