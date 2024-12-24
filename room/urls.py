from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()
router.register(r'room', api.RoomViewSet)
router.register(r'check-in', api.CheckInViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
