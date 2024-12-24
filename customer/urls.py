from django.urls import include, path
from rest_framework import routers

from customer.api import CostumerViewSet

router = routers.DefaultRouter()
router.register(r'customer', CostumerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
