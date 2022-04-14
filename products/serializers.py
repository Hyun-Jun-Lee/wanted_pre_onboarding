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
            'funding_amount',
            'publisher',
            'supporter',
            'supporter_count',
            'd_day'
            ]