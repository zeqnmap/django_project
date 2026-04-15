from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest
from datetime import datetime

from .forms import ProductForm, OrderForm
from .models import Product, Order


def shop_index(request: HttpRequest):
    products = [
        {
            'name': 'Ноутбук',
            'price': 75000,
            'description': 'Мощный ноутбук для игр',
            'created_at': datetime(2023, 6, 10)
        },
        {
            'name': 'Смартфон',
            'price': 35000,
            'description': 'Современный смартфон',
            'created_at': datetime(2026, 8, 15)
        },
        {
            'name': 'Наушники',
            'price': 5000,
            'description': 'Беспроводные наушники',
            'created_at': datetime(2026, 2, 20)
        },
    ]
    context = {'products': products}
    return render(request, 'shopapp/index.html', context=context)


def groups_list(request: HttpRequest):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all()
    }
    return render(request, 'shopapp/groups-list.html', context=context)


def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all()
    }
    return render(request, 'shopapp/products-list.html', context=context)


def create_product(request: HttpRequest):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:products_list")
            return redirect(url)
    else:
        form = ProductForm()
    context = {
        "form": form,
    }
    return render(request, 'shopapp/create-product.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all()
    }
    return render(request, 'shopapp/orders-list.html', context=context)


def create_orders(request: HttpRequest):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse("shopapp:orders_list")
            return redirect(url)
    else:
        form = OrderForm()
    context = {
        "form": form,
    }
    return render(request, 'shopapp/create-order.html', context=context)