from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import *
from .permissions import IsOwnerAccount, IsAnonymous
from .models import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (IsAnonymous,)

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.data)
        return Response({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'login': user.username,
            'pin': '0000'
        })


class UserIsOwnerChangePin(generics.UpdateAPIView, generics.GenericAPIView):
    serializer_class = UserChangePinSerializer
    permission_classes = (IsOwnerAccount,)

    def put(self, request, *args, **kwargs):
        user = self.request.user.pk
        instance = User.objects.get(pk=user)
        serializer = UserChangePinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.update(instance, serializer.validated_data)
        return Response({'result': result})


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
