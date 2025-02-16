from typing import Optional
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from shop.models import Product, Category, Order
from shop.forms import OrderForm, ProductModelForm


class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'


class OrderCreateView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = OrderForm()
        return render(request, 'shop/detail.html', {'form': form, 'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if product.quantity >= quantity:
                product.quantity -= quantity
                product.save()
                order = form.save(commit=False)
                order.product = product
                order.save()
                messages.success(request, 'Order successful sent')
            else:
                messages.error(request, 'Not enough stock available')
        return redirect('product_detail', pk=pk)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'shop/update.html'
    success_url = reverse_lazy('products')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'shop/update.html'
    success_url = reverse_lazy('products')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'shop/crud.html'
    success_url = reverse_lazy('products')