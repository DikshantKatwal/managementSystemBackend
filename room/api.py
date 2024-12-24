from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.serializers import Costumer, CostumerSerializer
from .models import Room, CheckIn
from .serializers import RoomSerializer, CheckInSerializer


class TwentyPageNumberPagination(PageNumberPagination):
    page_size = 12


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TwentyPageNumberPagination

    def list(self, request, *args, **kwargs):
        rooms = self.get_queryset().order_by('sequence')
        paginator = self.pagination_class()
        paginated_rooms = paginator.paginate_queryset(rooms, request)
        serializer = self.get_serializer(paginated_rooms, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='active-rooms')
    def fetch_active_rooms(self, request):
        rooms = self.get_queryset().filter(status=True)
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckInViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        customer_contact = data.get('contact')
        customer = Costumer.objects.filter(contact=customer_contact).first()
        if customer:
            return self.customer_check_in(data, customer)
        else:
            return self.customer_check_in(data)

    def customer_check_in(self, data, customer=None):
        if customer:
            customer_serializer = CostumerSerializer(instance=customer, data=data)
        else:
            customer_serializer = CostumerSerializer(data=data, partial=True)
        customer_serializer.is_valid(raise_exception=True)

        check_in_serializer = self.get_serializer(data=data, partial=True)
        check_in_serializer.is_valid(raise_exception=True)
        customer = customer_serializer.save()
        check_in = check_in_serializer.save(customer=customer, created_by=self.request.user.id)
        room = check_in.room
        room.status = False
        room.save()
        return Response(status=status.HTTP_201_CREATED)

    def create_payments(self, check_in, data):
        try:
            agreed_price = data['agreed_price']
            room_price = data['room_price']
            advance = data['advance']
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckOutViewSet(viewsets.ModelViewSet):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [IsAuthenticated]
