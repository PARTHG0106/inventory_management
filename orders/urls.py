from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path('<int:pk>/complete/', views.OrderCompleteView.as_view(), name='order_complete'),
    path('<int:pk>/cancel/', views.OrderCancelView.as_view(), name='order_cancel'),
] 