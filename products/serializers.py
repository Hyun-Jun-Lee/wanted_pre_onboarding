from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'pk',
            'title',
            'publisher',
            'publisher_username',
            'total_funding_amount',
            'funding_rate',
            'd_day',
            'description',
            'goal_amount',
            'closing_date',
            'onetime_funding_amount',
            'supporter_count',
            'created_at',
            'updated_at'
            ]
        read_only_fields = ('total_funding_amount',)
        extra_kwargs = {
            'publisher' : {'write_only':True}
        }
        
class ProductDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'title',
            'publisher',
            'publisher_username',
            'total_funding_amount',
            'funding_rate',
            'd_day',
            'description',
            'goal_amount',
            'supporter_count',
            'closing_date',
            'onetime_funding_amount',
            'created_at',
            'updated_at'
            ]
        read_only_fields = ('total_funding_amount','goal_amount')
        extra_kwargs = {
            'publisher' : {'write_only':True}
        }
        
class FundingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'supporter',
            'goal_amount',
            'supporter_count',
            'total_funding_amount',
            'onetime_funding_amount',
            'funding_rate',
            'd_day',
        ]
        read_only_fields = ('total_funding_amount','goal_amount')
        extra_kwargs = {
            'supporter' : {'write_only':True}
        }
        
    def update(self, instance, validated_data):
        instance.total_funding_amount += instance.onetime_funding_amount
        instance.save()
        return instance