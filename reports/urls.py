from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('sales/', views.SalesReportView.as_view(), name='sales'),
    path('inventory/', views.InventoryReportView.as_view(), name='inventory'),
    path('customers/', views.CustomerReportView.as_view(), name='customers'),
] 