from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', UserIsOwnerViewSet.as_view({'get': 'retrieve'})),
    path('create-user/', UserCreateAPIView.as_view()),

]
