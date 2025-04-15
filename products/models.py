from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import qrcode
from io import BytesIO
from django.core.files import File
import os
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class Category(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']
        
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    price = models.DecimalField(
        _('price'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    cost = models.DecimalField(
        _('cost'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    stock_quantity = models.IntegerField(
        _('stock quantity'),
        default=0,
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name=_('category')
    )
    sku = models.CharField(_('SKU'), max_length=50, unique=True)
    image = models.ImageField(
        _('image'),
        upload_to='products/',
        blank=True,
        null=True
    )
    qr_code = models.ImageField(
        _('QR code'),
        upload_to='qr_codes/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        if not self.sku:
            self.sku = f"{slugify(self.name)}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.sku)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            
            filename = f'qr-{self.sku}.png'
            self.qr_code.save(filename, File(buffer), save=False)
        
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    def is_low_stock(self):
        return self.stock_quantity <= 10
        
    def get_profit_margin(self):
        if self.cost > 0:
            return ((self.price - self.cost) / self.cost) * 100
        return 0
        
    @property
    def stock_status(self):
        if self.stock_quantity == 0:
            return 'out_of_stock'
        elif self.is_low_stock():
            return 'low_stock'
        return 'in_stock'
        
    @property
    def stock_status_display(self):
        status_map = {
            'out_of_stock': 'Out of Stock',
            'low_stock': 'Low Stock',
            'in_stock': 'In Stock'
        }
        return status_map.get(self.stock_status, 'Unknown')

class InventoryPermission(models.Model):
    class Meta:
        permissions = [
            ("manage_inventory", "Can manage inventory"),
            ("view_inventory", "Can view inventory"),
            ("update_inventory", "Can update inventory"),
            ("delete_inventory", "Can delete inventory"),
        ]
