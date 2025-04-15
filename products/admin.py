from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'cost', 'get_profit_margin', 'stock_quantity', 'get_stock_status', 'created_at')
    list_filter = ('category', 'is_deleted', 'created_at')
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'qr_code')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description', 'sku')
        }),
        (_('Pricing'), {
            'fields': ('price', 'cost')
        }),
        (_('Inventory'), {
            'fields': ('stock_quantity',)
        }),
        (_('Media'), {
            'fields': ('image', 'qr_code')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_deleted=False)
    
    def has_delete_permission(self, request, obj=None):
        return False
        
    def get_stock_status(self, obj):
        return obj.stock_status_display
    get_stock_status.short_description = _('Stock Status')
    get_stock_status.admin_order_field = 'stock_quantity'
    
    def get_profit_margin(self, obj):
        return f"{obj.get_profit_margin():.2f}%"
    get_profit_margin.short_description = _('Profit Margin')
    get_profit_margin.admin_order_field = 'price'
