from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "products"

urlpatterns =[
    path("products", views.ProductListAPIView.as_view()),
    path("products/<int:pk>", views.ProductDetailAPIView.as_view()),
    path("products/<int:pk>/funding", views.FundingAPIView.as_view()),
]