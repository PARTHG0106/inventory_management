from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from products.models import Product
from suppliers.models import Supplier
from customers.models import Customer
from orders.models import Order

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint for products."""
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter products based on user permissions."""
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(is_active=True)
    
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Update product stock level."""
        product = self.get_object()
        quantity = request.data.get('quantity')
        if quantity is not None:
            product.stock_level = quantity
            product.save()
            return Response({'status': 'stock updated'})
        return Response({'error': 'quantity required'}, status=400)

class SupplierViewSet(viewsets.ModelViewSet):
    """API endpoint for suppliers."""
    queryset = Supplier.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter suppliers based on user permissions."""
        if self.request.user.is_superuser:
            return Supplier.objects.all()
        return Supplier.objects.filter(is_active=True)

class CustomerViewSet(viewsets.ModelViewSet):
    """API endpoint for customers."""
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter customers based on user permissions."""
        if self.request.user.is_superuser:
            return Customer.objects.all()
        return Customer.objects.filter(is_active=True)

class OrderViewSet(viewsets.ModelViewSet):
    """API endpoint for orders."""
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter orders based on user permissions."""
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order."""
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            return Response({'status': 'order cancelled'})
        return Response({'error': 'can only cancel pending orders'}, status=400)
