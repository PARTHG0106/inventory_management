from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import Permission

class ActivityLog(models.Model):
    """Model for tracking system activities."""
    
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('restore', 'Restore'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Password Change'),
        ('password_reset', 'Password Reset'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        verbose_name=_('user')
    )
    action = models.CharField(
        _('action'),
        max_length=20,
        choices=ACTION_CHOICES
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    details = models.TextField(_('details'), blank=True)
    ip_address = models.GenericIPAddressField(_('IP address'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('activity log')
        verbose_name_plural = _('activity logs')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_action_display()} by {self.user} at {self.created_at}"
        
    @classmethod
    def log_activity(cls, user, action, content_object=None, details='', ip_address=None):
        """Create a new activity log entry."""
        content_type = None
        object_id = None
        
        if content_object:
            content_type = ContentType.objects.get_for_model(content_object)
            object_id = content_object.id
            
        return cls.objects.create(
            user=user,
            action=action,
            content_type=content_type,
            object_id=object_id,
            details=details,
            ip_address=ip_address
        )

class DashboardPermission(models.Model):
    """Model to handle dashboard access permissions."""
    class Meta:
        permissions = [
            ("view_dashboard", "Can view dashboard"),
            ("view_own_dashboard", "Can view own dashboard"),
        ]
