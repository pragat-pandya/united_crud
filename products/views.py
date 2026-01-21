from django.shortcuts import render
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsProductOwner
# Create your views here.


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Set the user who created the product"""
        serializer.save(added_by=self.request.user)


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsProductOwner]