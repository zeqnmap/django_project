from django.shortcuts import render
from datetime import datetime

def product_list(request):
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
            'description': 'Беспроводные наушники с шумоподавлением',
            'created_at': datetime(2026, 2, 20)
        },
    ]
    context = {'products': products}
    return render(request, 'shopapp/index.html', context=context)