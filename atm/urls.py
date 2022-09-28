from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)
router.register(r'wallet', UserWalletViewSet, basename='wallet')

urlpatterns = [
    path('', include(router.urls)),
    path('', UserIsOwnerViewSet.as_view({'get': 'retrieve'})),
    path('balance/', CardBalanceAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('change-pin/', UserIsOwnerChangePin.as_view()),

]
