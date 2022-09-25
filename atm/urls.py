from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', UserIsOwnerViewSet.as_view({'get': 'retrieve'})),
    path('wallet/', UserWalletListAPIView.as_view()),
    path('new-card/', CardCreateAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
    path('change-pin/', UserIsOwnerChangePin.as_view()),

]
