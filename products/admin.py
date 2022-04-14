from django.contrib import admin
from .models import Product
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
            'title',
            'description',
            'goal_amount',
            'closing_date',
            'funding_amount',
            'publisher',
            'supporter_count',
            'd_day'
            ]
