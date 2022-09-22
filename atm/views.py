from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import *
from .permissions import IsOwnerAccount
from .models import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class UserIsOwnerViewSet(viewsets.ModelViewSet):
    serializer_class = UserIsOwnerDetailSerializer
    permission_classes = (IsOwnerAccount,)

    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = User.objects.get(pk=self.request.user.pk)
        except models.ObjectDoesNotExist:
            return Response({'error': 'error'})
        serializer = UserIsOwnerDetailSerializer(queryset)
        return Response(serializer.data)
