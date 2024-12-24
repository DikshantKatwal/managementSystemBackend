from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from employee.models import Employee
from employee.serializers import EmployeeSerializer
from users.api import create_user
from users.serializers import UserSerializer


class EmployeeDetails(generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employee_id = request.query_params.get('id')
            if employee_id:
                employee = self.get_queryset().filter(id=employee_id).first()
                if not employee:
                    raise NotFound("Employee not found")
                serializer = self.get_serializer(employee)
            else:
                employees = self.get_queryset()
                serializer = self.get_serializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('Something Went Wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            serializer = self.get_serializer(data=data, partial=True)
            if serializer.is_valid():
                user = create_user(request.data)
                serializer.save(created_by=request.user.id, updated_by=request.user.id, user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('Something Went Wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            data = request.data
            if 'id' not in data:
                return Response('id not found', status=status.HTTP_400_BAD_REQUEST)
            employee = self.get_queryset().filter(id=data['id']).first()
            serializer = self.get_serializer(instance=employee, data=data, partial=True)
            user_serializer = UserSerializer(employee.user, data=data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_serializer.save()
            return Response('serializer.data', status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('Something Went Wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
