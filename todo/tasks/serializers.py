from rest_framework import serializers

from todo.tasks.models import Task
from todo.users.serializers import UserRetrieveSerializer


class TaskSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer(read_only=True)
    tags = serializers.CharField(source="get_tags_display")

    class Meta:
        model = Task
        fields = ("id", "title", "is_completed", "user", "tags", "created_at", "updated_at")


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


class TaskTagsSerializer(serializers.Serializer):
    tags = serializers.CharField(allow_blank=True)
