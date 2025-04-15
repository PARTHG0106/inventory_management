from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from users.models import CustomUser

class Supplier(models.Model):
    """Supplier model for managing product suppliers."""
    
    name = models.CharField(_('name'), max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20)
    address = models.TextField(_('address'))
    city = models.CharField(_('city'), max_length=100)
    state = models.CharField(_('state'), max_length=100)
    country = models.CharField(_('country'), max_length=100)
    postal_code = models.CharField(_('postal code'), max_length=20)
    tax_id = models.CharField(_('tax ID'), max_length=50, blank=True)
    website = models.URLField(_('website'), blank=True)
    notes = models.TextField(_('notes'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_deleted = models.BooleanField(_('deleted'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = _('supplier')
        verbose_name_plural = _('suppliers')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def soft_delete(self):
        """Soft delete the supplier."""
        self.is_deleted = True
        self.save()
        
    def restore(self):
        """Restore a soft-deleted supplier."""
        self.is_deleted = False
        self.save()
        
    def get_total_orders(self):
        """Get total number of purchase orders."""
        return self.purchase_orders.count()
        
    def get_total_spent(self):
        """Get total amount spent with this supplier."""
        from orders.models import PurchaseOrder
        return PurchaseOrder.objects.filter(
            supplier=self,
            status='completed'
        ).aggregate(total=models.Sum('total_amount'))['total'] or 0
        
    def get_active_products(self):
        """Get all active products supplied by this supplier."""
        from products.models import Product
        return Product.objects.filter(
            supplier=self,
            status='active',
            is_deleted=False
        )

    def delete(self, *args, **kwargs):
        """Override delete to prevent deletion by non-superusers."""
        request = kwargs.pop('request', None)
        if request and not request.user.is_superuser:
            raise PermissionDenied("Only superusers can delete suppliers")
        super().delete(*args, **kwargs)
