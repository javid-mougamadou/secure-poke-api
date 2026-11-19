from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GroupTypePathParamSerializer, UserMeSerializer


class GroupAddAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, type):
        """
        group_add

        A View for adding the current user to the <type> group
        """
        serializer = GroupTypePathParamSerializer(data={'type': type})
        serializer.is_valid(raise_exception=True)
        group = Group.objects.get(name=serializer.validated_data['type'])
        request.user.groups.add(group)
        return Response(status=204)


class GroupRemoveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, type):
        """
        group_remove

        A View for removing the current user from the <type> group
        """
        serializer = GroupTypePathParamSerializer(data={'type': type})
        serializer.is_valid(raise_exception=True)
        group = Group.objects.get(name=serializer.validated_data['type'])
        request.user.groups.remove(group)
        return Response(status=204)


class UserMeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        user_me

        A View for retrieving the current user and the Pokemon types they belong to
        """
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)


class LoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        login

        A View for authenticating a user and returning their token
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
