from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type',
        'email',
        'phone',
        'is_active',
        'is_deleted'
    )
    list_filter = (
        'type',
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
                'type',
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
        queryset.update(is_deleted=True)
        self.message_user(
            request,
            _('Successfully soft deleted selected customers.')
        )
    soft_delete_selected.short_description = _('Soft delete selected customers')
    
    def restore_selected(self, request, queryset):
        queryset.update(is_deleted=False)
        self.message_user(
            request,
            _('Successfully restored selected customers.')
        )
    restore_selected.short_description = _('Restore selected customers')
    
    def get_queryset(self, request):
        return super().get_queryset(request)
        
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('customers.change_customer')
    
    def has_add_permission(self, request):
        return request.user.has_perm('customers.add_customer')
    
    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('customers.view_customer')
    
    def delete_model(self, request, obj):
        if not request.user.is_superuser:
            raise PermissionDenied("Only superusers can delete customers")
        obj.delete(request=request)
    
    def delete_queryset(self, request, queryset):
        if not request.user.is_superuser:
            raise PermissionDenied("Only superusers can delete customers")
        for obj in queryset:
            obj.delete(request=request)
