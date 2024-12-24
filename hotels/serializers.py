from rest_framework import serializers

from hotels.models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ['deleted_at', 'restored_at', "transaction_id", "created_by", "updated_by", "deleted_by",
                   "created_at", "updated_at"]
