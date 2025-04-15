from django import forms
from .models import Supplier
from django.utils.translation import gettext_lazy as _

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name', 'email', 'phone',
            'address', 'city', 'state',
            'country', 'postal_code',
            'tax_id', 'website', 'notes',
            'is_active'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': _('Name'),
            'email': _('Email Address'),
            'phone': _('Phone Number'),
            'address': _('Address'),
            'city': _('City'),
            'state': _('State'),
            'country': _('Country'),
            'postal_code': _('Postal Code'),
            'tax_id': _('Tax ID'),
            'website': _('Website'),
            'notes': _('Notes'),
            'is_active': _('Active')
        } 