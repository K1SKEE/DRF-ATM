from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .permissions import IsOwnerAccount, IsAnonymous
from .models import *
from .utils import ViewSetMixin, TransactionPagination, get_currency_rate


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
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


class UserIsOwnerChangePin(generics.UpdateAPIView):
    serializer_class = UserChangePinSerializer
    permission_classes = (IsOwnerAccount,)

    def put(self, request, *args, **kwargs):
        user = request.user.pk
        instance = User.objects.get(pk=user)
        serializer = UserChangePinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.update(instance, serializer.validated_data)
        return Response({'result': result})


class UserIsOwnerViewSet(viewsets.ModelViewSet):
    serializer_class = UserIsOwnerDetailSerializer
    permission_classes = (IsOwnerAccount,)

    def retrieve(self, request, *args, **kwargs):
        queryset = User.objects.get(pk=request.user.pk)
        serializer = UserIsOwnerDetailSerializer(queryset)
        return Response(serializer.data)


class UserWalletViewSet(ViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (IsOwnerAccount,)

    def get_queryset(self):
        user = self.request.user
        return user.wallet.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CardCreateSerializer
        return WalletSerializer

    def create(self, request, *args, **kwargs):
        serializer = CardCreateSerializer(data=request.data,
                                          context={'request': request})
        serializer.is_valid(raise_exception=False)
        result = serializer.create(serializer.validated_data)
        return Response({'result': result})

    @action(methods=['POST'], detail=False)
    def balance(self, request):
        serializer = CardBalanceSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = Card.objects.get(card_number=serializer.data.get('card'))
        if instance.user == request.user:
            result = serializer.get_balance(instance)
            return Response({'result': result})
        raise Http404

    @action(methods=['PUT'], detail=False)
    def deposit(self, request):
        return self.put_mixin(request, CardDepositSerializer, 'card')

    @action(methods=['PUT'], detail=False)
    def withdraw(self, request):
        return self.put_mixin(request, CardWithdrawSerializer, 'card')

    @action(methods=['PUT'], detail=False)
    def send_money(self, request):
        return self.put_mixin(request, CardSendMoneySerializer, 'card_sender')


class TransactionListAPIView(generics.ListAPIView):
    permission_classes = (IsOwnerAccount,)
    serializer_class = TransactionListSerializer
    pagination_class = TransactionPagination

    def get_queryset(self):
        user = self.request.user
        return user.transaction.all()


class CurrencyRate(APIView):
    @staticmethod
    def get(request):
        currency_rate = get_currency_rate()
        print(currency_rate['usd_buy'])
        return Response(get_currency_rate())
