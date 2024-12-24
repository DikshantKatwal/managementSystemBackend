from rest_framework import serializers

from .models import Room, CheckIn, CheckInHistory


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_no', 'price', 'status']


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = '__all__'


class CheckInHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckInHistory
        fields = '__all__'
