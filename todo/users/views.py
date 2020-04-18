from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from todo.users.models import User
from todo.users.serializers import (
    UserLoginSerializer, UserSerializer, UserRetrieveSerializer, UserUpdateSerializer
)


class UserLoginView(APIView):
    """
    Use this endpoint to login user (create user authentication token).
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.user)
            data = UserRetrieveSerializer(instance=serializer.user).data
            data.update({
                "auth_token": token.key
            })
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """
    Use this endpoint to logout user (remove user authentication token).
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)


class UserDetailView(RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method.lower() == "get":
            return UserRetrieveSerializer
        elif  self.request.method.lower() in ["put", "patch"]:
            return UserUpdateSerializer
        else:
            return UserSerializer
