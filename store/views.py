from django.shortcuts import render
from .models import Product, Category
from django.contrib import messages
from django.db.models import Q
# Create your views here.
def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        # Query from database the product
        searched = Product.objects.filter(Q(name__icontains = searched) | Q(description__icontains = searched))
        if not searched:
            messages.success(request, "Không tìm thấy sản phẩm")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {
            'searched': searched
        })
    else:
        return render(request, 'search.html', {})

def fruits(request):
    fruits = Category.objects.get(name='Trái cây')
    products = Product.objects.filter(category = fruits)
    return render(request, 'fruits.html', {
        'products': products
    })

def meat(request):
    meat = Category.objects.get(name='Thịt')
    products = Product.objects.filter(category = meat)
    return render(request, 'meat.html', {
        'products': products
    })

def vegetables(request):
    vegetables = Category.objects.get(name='Rau củ')
    products = Product.objects.filter(category = vegetables)
    return render(request, 'vegetables.html', {
        'products': products
    })

def seafood(request):
    seafood = Category.objects.get(name='Hải sản')
    products = Product.objects.filter(category = seafood)
    return render(request, 'seafood.html', {
        'products': products
    })

# def category(request, ctgy):
#     category = Category.objects.get(name=ctgy)
#     products = Product.objects.filter(category=category)
#     return render(request, 'layout.html', {
#         'products': products
#     })

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'chitietsanpham.html', {
        'product': product
    })