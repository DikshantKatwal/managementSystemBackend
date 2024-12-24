from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customer.models import Costumer
from customer.serializers import CostumerSerializer


class TwentyPageNumberPagination(PageNumberPagination):
    page_size = 20


class CostumerViewSet(viewsets.ModelViewSet):
    queryset = Costumer.objects.all()
    serializer_class = CostumerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TwentyPageNumberPagination

    def list(self, request, *args, **kwargs):
        customers = self.get_queryset()
        paginator = self.pagination_class()
        paginated_customers = paginator.paginate_queryset(customers, request)
        serializer = self.get_serializer(paginated_customers, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get-contacts')
    def get_contacts(self, request, *args, **kwargs):
        contacts = list(Costumer.objects.values_list("contact", flat=True))
        return Response(contacts, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='get-customer')
    def get_customer_w_contact(self, request):
        contact = request.query_params.get('contact')
        if not contact:
            return Response('contact is required', status=status.HTTP_400_BAD_REQUEST)
        customer = self.queryset.filter(contact=contact).first()
        if not customer:
            return Response('Customer Not Found', status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance=customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('Invalid Data', status=status.HTTP_400_BAD_REQUEST)
