from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
from orders.models import Order
from customers.models import Customer
from suppliers.models import Supplier

# Create your views here.

@login_required
def dashboard(request):
    # Get basic statistics
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock_quantity__lt=10).count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_customers = Customer.objects.count()
    total_suppliers = Supplier.objects.count()

    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_customers': total_customers,
        'total_suppliers': total_suppliers,
    }
    
    return render(request, 'core/dashboard.html', context)
