from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('import/', views.ProductImportView.as_view(), name='product_import'),
    path('export/', views.ProductExportView.as_view(), name='product_export'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
] 