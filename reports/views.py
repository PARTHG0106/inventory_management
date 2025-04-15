from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from orders.models import Order
from products.models import Product
from customers.models import Customer
from django.db import models


class ReportListView(LoginRequiredMixin, ListView):
    template_name = 'reports/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return [
            {
                'name': 'Sales Report',
                'description': 'View sales data and trends',
                'url': 'sales'
            },
            {
                'name': 'Inventory Report',
                'description': 'View inventory levels and stock movements',
                'url': 'inventory'
            },
            {
                'name': 'Customer Report',
                'description': 'View customer data and purchase history',
                'url': 'customers'
            }
        ]

class SalesReportView(LoginRequiredMixin, View):
    template_name = 'reports/sales_report.html'

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date or not end_date:
            end_date = timezone.now().date()
            start_date = end_date - timedelta(days=30)
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        orders = Order.objects.filter(
            created_at__date__range=[start_date, end_date],
            status='completed'
        )

        total_orders = orders.count()
        total_revenue = sum(order.total for order in orders)
        average_order_value = total_revenue / total_orders if total_orders > 0 else 0

        context = {
            'start_date': start_date,
            'end_date': end_date,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'average_order_value': average_order_value,
            'orders': orders
        }

        return render(request, self.template_name, context)

class InventoryReportView(LoginRequiredMixin, View):
    template_name = 'reports/inventory_report.html'

    def get(self, request):
        low_stock_products = Product.objects.filter(stock__lt=10)
        
        out_of_stock_products = Product.objects.filter(stock=0)
        
        total_inventory_value = sum(product.stock * product.price for product in Product.objects.all())

        context = {
            'low_stock_products': low_stock_products,
            'out_of_stock_products': out_of_stock_products,
            'total_inventory_value': total_inventory_value
        }

        return render(request, self.template_name, context)

class CustomerReportView(LoginRequiredMixin, View):
    template_name = 'reports/customer_report.html'

    def get(self, request):
        top_customers = Customer.objects.annotate(
            order_count=models.Count('orders'),
            total_spent=models.Sum('orders__total')
        ).order_by('-total_spent')[:10]

        customer_growth = Customer.objects.annotate(
            month=models.functions.TruncMonth('created_at')
        ).values('month').annotate(
            count=models.Count('id')
        ).order_by('month')

        context = {
            'top_customers': top_customers,
            'customer_growth': customer_growth
        }

        return render(request, self.template_name, context)
