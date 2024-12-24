from django.contrib.auth import authenticate
from rest_framework import serializers

from employee.serializers import EmployeeSerializer
from users.models import NewUser


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        try:
            user = authenticate(email=email, password=password)
        except NewUser.DoesNotExist:
            raise serializers.ValidationError("No user found for this email in the current company.")
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials.")


def get_formated_date(obj):
    """
    Format the date in a human-readable format.
    """
    if obj:
        return obj.strftime('%I %p, %d %b %Y ')  # Example: 7 AM, 22 March 2027
    return None


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    employee_data = EmployeeSerializer(source='employee_user', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = NewUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = NewUser.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['last_login_formatted'] = get_formated_date(instance.last_login)
        return representation

    # def get_full_name(self, obj):
    #     return f"{obj.first_name} {obj.last_name}".strip()
