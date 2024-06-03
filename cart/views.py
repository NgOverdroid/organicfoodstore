from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products
    cart_quantities = cart.get_quantities
    totals = cart.total()
    return render(request, "cart_summary.html", {
        "cart_products": cart_products,
        "quantities": cart_quantities,
        "totals": totals
    })

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id) #look up product in the database, return 404 if 
        cart.add(product=product, quantity = product_qty)    #Save to session
        response = JsonResponse({'Product Name: ': product.name})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
    cart.delete(product=product_id)
    response = JsonResponse({'Product ID: ': product_id})
    return response

def cart_update(request):
    pass