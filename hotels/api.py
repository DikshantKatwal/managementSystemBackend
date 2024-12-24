from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hotels.models import Hotel
from hotels.serializers import HotelSerializer
from settings.decorators import IsSuperuser
from users.api import UserCreateAPI


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'name' not in data:
            return Response('Name is required', status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)  # Save both user and hotel in one go
            return Response('Saved successfully', status=status.HTTP_201_CREATED)
        else:
            return Response('Invalid Data', status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # Create the user first
        user = UserCreateAPI.create_user(self.request)

        # Add the user id to the hotel (company_id) and save the hotel
        # Pass user.id directly in the serializer data
        serializer.save(company_id=user.id)
