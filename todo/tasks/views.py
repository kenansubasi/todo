from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todo.tasks.models import Task
from todo.tasks.serializers import (
    TaskSerializer, TaskListSerializer, TaskCreateSerializer, TaskRetrieveSerializer, TaskUpdateSerializer,
    TaskTagsSerializer
)


class TaskListView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("is_completed",)
    search_fields = ("title",)

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


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "task_id"

    def get_queryset(self):
        return Task.objects.select_related("user").filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return TaskRetrieveSerializer
        elif  self.request.method.lower() in ["put", "patch"]:
            return TaskUpdateSerializer
        else:
            return TaskSerializer


class TaskTagsSetView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = "task_id"

    def get_queryset(self):
        return Task.objects.select_related("user").filter(user=self.request.user).order_by("-id")

    def post(self, request, *args, **kwargs):
        serializer = TaskTagsSerializer(data=request.data)

        if serializer.is_valid():
            instance = self.get_object()
            tag_list = serializer.validated_data.get("tags", "")
            if tag_list:
                instance.tags.set(*tag_list.split(","))
            else:
                instance.tags.clear()
            return Response(request.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
