from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from .models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'is_active',
        'is_deleted'
    )
    list_filter = (
        'is_active',
        'is_deleted',
        'created_at',
        'updated_at'
    )
    search_fields = (
        'name',
        'email',
        'phone',
        'address'
    )
    readonly_fields = (
        'created_at',
        'updated_at'
    )
    
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'email',
                'phone'
            )
        }),
        (_('Address'), {
            'fields': (
                'address',
                'city',
                'state',
                'country',
                'postal_code'
            )
        }),
        (_('Additional Information'), {
            'fields': (
                'tax_id',
                'website',
                'notes'
            )
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
        (_('Timestamps'), {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
        (_('Soft Delete'), {
            'fields': ('is_deleted',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['soft_delete_selected', 'restore_selected']
    
    def soft_delete_selected(self, request, queryset):
        if not request.user.has_perm('suppliers.change_supplier'):
            raise PermissionDenied("You don't have permission to change suppliers")
        queryset.update(is_deleted=True)
    soft_delete_selected.short_description = _("Soft delete selected suppliers")
    
    def restore_selected(self, request, queryset):
        if not request.user.has_perm('suppliers.change_supplier'):
            raise PermissionDenied("You don't have permission to change suppliers")
        queryset.update(is_deleted=False)
    restore_selected.short_description = _("Restore selected suppliers")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(is_deleted=False)
        return qs
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('suppliers.change_supplier')
    
    def has_add_permission(self, request):
        return request.user.has_perm('suppliers.add_supplier')
    
    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('suppliers.view_supplier')
    
    def delete_model(self, request, obj):
        if not request.user.is_superuser:
            raise PermissionDenied("Only superusers can delete suppliers")
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        if not request.user.is_superuser:
            raise PermissionDenied("Only superusers can delete suppliers")
        super().delete_queryset(request, queryset)
