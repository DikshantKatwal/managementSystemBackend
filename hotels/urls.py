from django.urls import include, path
from rest_framework import routers

from hotels.api import HotelViewSet

router = routers.DefaultRouter()
router.register(r'hotel', HotelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
