from rest_framework import serializers

from customer.models import Costumer


class CostumerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = Costumer
        # fields = '__all__'
        exclude = ['deleted_at', 'restored_at', 'transaction_id', 'updated_at', 'created_at', 'deleted_by',
                   'updated_by', 'created_by']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['full_name'] = f'{instance.first_name} {instance.last_name}'
    #     return representation
