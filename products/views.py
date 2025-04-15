from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
from .models import Product, Category
from .forms import ProductForm, ProductImportForm
import csv
from django.utils import timezone

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')
    success_message = "Product was created successfully"

class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')
    success_message = "Product was updated successfully"

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')

class ProductImportView(LoginRequiredMixin, FormView):
    template_name = 'products/product_import.html'
    form_class = ProductImportForm
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        csv_file = form.cleaned_data['csv_file']
        decoded_file = csv_file.read().decode('utf-8')
        reader = csv.DictReader(decoded_file.splitlines())
        
        for row in reader:
            Product.objects.create(
                name=row['name'],
                description=row['description'],
                price=float(row['price']),
                stock_quantity=int(row['stock_quantity']),
                category=row['category'],
                sku=row['sku']
            )
        
        return super().form_valid(form)

class ProductExportView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_export.html'

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="products_{timezone.now().strftime("%Y%m%d")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Description', 'Price', 'Stock Quantity', 'Category', 'SKU'])
        
        for product in self.get_queryset():
            writer.writerow([
                product.name,
                product.description,
                product.price,
                product.stock_quantity,
                product.category,
                product.sku
            ])
        
        return response

@method_decorator(require_POST, name='dispatch')
class CategoryCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if not name:
            return JsonResponse({'success': False, 'error': 'Category name is required'})
            
        try:
            category = Category.objects.create(
                name=name,
                description=description
            )
            return JsonResponse({
                'success': True,
                'category': {
                    'id': category.id,
                    'name': category.name
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
