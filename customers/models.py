from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from users.models import CustomUser

class Customer(models.Model):
    
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
    ]
    
    type = models.CharField(
        _('type'),
        max_length=20,
        choices=CUSTOMER_TYPE_CHOICES,
        default='individual'
    )
    name = models.CharField(_('name'), max_length=200)
    contact_person = models.CharField(_('contact person'), max_length=100, blank=True)
    email = models.EmailField(_('email'))
    phone = models.CharField(_('phone'), max_length=20)
    address = models.TextField(_('address'))
    city = models.CharField(_('city'), max_length=100)
    state = models.CharField(_('state'), max_length=100)
    country = models.CharField(_('country'), max_length=100)
    postal_code = models.CharField(_('postal code'), max_length=20)
    tax_id = models.CharField(_('tax ID'), max_length=50, blank=True)
    website = models.URLField(_('website'), blank=True)
    notes = models.TextField(_('notes'), blank=True)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)
    
    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        ordering = ['name']
        
    def __str__(self):
        return self.name
        
    def soft_delete(self):
        self.is_deleted = True
        self.save()
        
    def restore(self):
        self.is_deleted = False
        self.save()
        
    def get_total_orders(self):
        return self.sales_orders.count()
        
    def get_total_spent(self):
        from orders.models import SalesOrder
        return SalesOrder.objects.filter(
            customer=self,
            status='completed'
        ).aggregate(total=models.Sum('total_amount'))['total'] or 0
        
    def get_last_order_date(self):
        from orders.models import SalesOrder
        last_order = SalesOrder.objects.filter(
            customer=self
        ).order_by('-created_at').first()
        return last_order.created_at if last_order else None
        
    @property
    def is_business(self):
        return self.type == 'business'
        
    @property
    def is_individual(self):
        return self.type == 'individual'

    def delete(self, *args, **kwargs):
        from django.core.exceptions import PermissionDenied
        
        request = kwargs.pop('request', None)
        if request and not request.user.is_superuser:
            raise PermissionDenied("Only superusers can delete customers")
            
        if not request and not CustomUser.objects.filter(is_superuser=True).exists():
            raise PermissionDenied("Only superusers can delete customers")
            
        super().delete(*args, **kwargs)
