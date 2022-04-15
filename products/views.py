from functools import partial
from django.shortcuts import render
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Product
from .serializers import ProductSerializer, ProductDetailSerializer, FundingSerializer

# Create your views here.

class ProductListAPIView(generics.ListCreateAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'total_funding_amount']
    
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    
    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        if product.publisher.username != request.user.username:
            return Response("It's Not Your Room", status=status.HTTP_401_UNAUTHORIZED)
        product.delete()
        return Response("Delete Complete",status=status.HTTP_200_OK)

class FundingAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = FundingSerializer
    
        
    
