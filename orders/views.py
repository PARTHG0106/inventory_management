from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Order, OrderItem

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.select_related('customer').prefetch_related('items')

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.select_related('customer').prefetch_related('items')

class OrderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = ['customer', 'status', 'notes']
    success_url = reverse_lazy('orders:order_list')
    success_message = "Order was created successfully"

class OrderUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = ['customer', 'status', 'notes']
    success_url = reverse_lazy('orders:order_list')
    success_message = "Order was updated successfully"

class OrderDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders:order_list')
    success_message = "Order was deleted successfully"

class OrderCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.status != 'completed':
            order.status = 'completed'
            order.save()
            messages.success(request, f'Order #{order.id} has been marked as completed.')
        else:
            messages.warning(request, f'Order #{order.id} is already completed.')
        return redirect('orders:order_detail', pk=order.pk)

class OrderCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.status != 'cancelled':
            order.status = 'cancelled'
            order.save()
            messages.success(request, f'Order #{order.id} has been cancelled.')
        else:
            messages.warning(request, f'Order #{order.id} is already cancelled.')
        return redirect('orders:order_detail', pk=order.pk)