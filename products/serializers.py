from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'goal_amount',
            'closing_date',
            'onetime_funding_amount',
            'total_funding_amount',
            'publisher',
            'supporter',
            'supporter_count',
            'd_day',
            'created_at',
            'updated_at'
            ]
        read_only_fields = ('total_funding_amount',)