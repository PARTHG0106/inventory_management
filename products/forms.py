from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'cost', 'stock_quantity', 'category', 'sku', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'cost': forms.NumberInput(attrs={'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'min': '0'}),
        }

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not sku:
            name = self.cleaned_data.get('name', '')
            sku = name.upper().replace(' ', '')[:8] + '-' + str(Product.objects.count() + 1)
        return sku

class ProductImportForm(forms.Form):
    csv_file = forms.FileField(
        label='Select a CSV file',
        help_text='The CSV file should have columns: name, description, price, stock_quantity, category, sku'
    ) 