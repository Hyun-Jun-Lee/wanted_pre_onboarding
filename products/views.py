from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Product
from .serializers import ProductSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['@title']
    ordering_fields = ['created_at', 'total_funding_amount']
    
