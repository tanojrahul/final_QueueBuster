from rest_framework import serializers
from your_app.models import PaymentOrder

class PaymentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOrder
        fields = ['id', 'amount', 'currency', 'status', 'created_at']
