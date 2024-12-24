from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from employee.models import Employee
from employee.serializers import EmployeeSerializer
from users.models import NewUser
from users.serializers import LoginSerializer, UserSerializer


def create_user(data):
    """
    Utility to create a user using the UserSerializer.
    """
    user_serializer = UserSerializer(data=data)
    if user_serializer.is_valid(raise_exception=True):
        user = user_serializer.save()
        return user
    raise ValidationError(user_serializer.errors)


class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def get_user(self, request):
        ...

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            login(request, user)
            return Response({
                "message": "Login successful",
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "_token": AuthToken.objects.create(user)[1],
            })
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPI(generics.CreateAPIView):
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer

    @staticmethod
    def create_user(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  # This will raise an exception if validation fails
            user = serializer.save()
            return user  # Ensure user object is returned, not a Response object

    def post(self, request, *args, **kwargs):
        user = self.create_user(request)
        if isinstance(user, Response):  # Check if it's an error response
            return user
        return Response({
            "message": "User created successfully",
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class GetUserDetails(generics.GenericAPIView):
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            users = self.get_queryset()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('Something Went Wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            user = request.user
            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response('Something Went Wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            user = request.user
            data = request.data
            print(data)
            serializer = UserSerializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            employee = Employee.objects.filter(user=user).first()
            if employee:
                emp_serializer = EmployeeSerializer(instance=employee, data=data)
                emp_serializer.is_valid(raise_exception=True)
                emp_serializer.save(updated_by=user.id)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response('serializer.data', status=status.HTTP_400_BAD_REQUEST)

    def change_password(self, request):
        user = request.user
        password = request.data.get('password')
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
