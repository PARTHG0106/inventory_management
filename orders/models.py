from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal
from customers.models import Customer
from products.models import Product

class Order(models.Model):
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)
    total_amount = models.DecimalField(
        _('total amount'),
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'Order #{self.id} - {self.customer.name}'
        
    def soft_delete(self):
        self.is_deleted = True
        self.save()
        
    def restore(self):
        self.is_deleted = False
        self.save()
        
    @property
    def is_completed(self):
        return self.status == 'completed'
        
    @property
    def is_cancelled(self):
        return self.status == 'cancelled'

    @property
    def total(self):
        return sum(item.total for item in self.items.all())

    def calculate_total(self):
        return sum(item.price * item.quantity for item in self.items.all())

class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        _('quantity'),
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
        
    @property
    def total_price(self):
        return self.quantity * self.price

    @property
    def total(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
        self.order.total_amount = self.order.calculate_total()
        self.order.save()

class SalesOrder(Order):
    
    order_number = models.CharField(
        _('order number'),
        max_length=50,
        unique=True
    )
    
    class Meta:
        verbose_name = _('sales order')
        verbose_name_plural = _('sales orders')
        
    def __str__(self):
        return f"SO-{self.order_number}"
        
    def calculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.save()
        
    def update_stock(self):
        if self.status == 'completed':
            for item in self.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()

class SalesOrderItem(OrderItem):
    
    class Meta:
        verbose_name = _('sales order item')
        verbose_name_plural = _('sales order items')
        
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class PurchaseOrder(Order):
    
    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.PROTECT,
        related_name='purchase_orders',
        verbose_name=_('supplier')
    )
    order_number = models.CharField(
        _('order number'),
        max_length=50,
        unique=True
    )
    
    class Meta:
        verbose_name = _('purchase order')
        verbose_name_plural = _('purchase orders')
        
    def __str__(self):
        return f"PO-{self.order_number}"
        
    def calculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.save()
        
    def update_stock(self):
        if self.status == 'completed':
            for item in self.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()

class PurchaseOrderItem(OrderItem):
    
    class Meta:
        verbose_name = _('purchase order item')
        verbose_name_plural = _('purchase order items')
        
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"