from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from store.models import Product
from accounts.models import Profile
import datetime
from django.contrib import messages
# Create your views here.
def payment_success(request):
    return render(request, "payment_success.html", {})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products
    cart_quantities = cart.get_quantities
    totals = cart.total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "checkout.html", {
        "cart_products": cart_products,
        "quantities": cart_quantities,
        "totals": totals,
        "shipping_form": shipping_form
    })
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "checkout.html", {
        "cart_products": cart_products,
        "quantities": cart_quantities,
        "totals": totals,
        "shipping_form":shipping_form
    })
    
def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quantities
        totals = cart.total()

        payment_form = PaymentForm(request.POST or None) #get card info from billing_info.html
        my_shipping = request.session.get('my_shipping') # Get Shipping Session Data from billing_info()
        
        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

        # Create Shipping address from session info
        shipping_address = f"{my_shipping['shipping_address']}"
        amount_paid = totals['big_sum']

        #Create an order
        if request.user.is_authenticated:
            user = request.user

            #Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

			# Add order items
			
			# Get the order ID
            order_id = create_order.pk
            # Get product info
            for product in cart_products():
                product_id = product.id
                price = product.price
                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()
            
            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            # Delete Cart from Database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database (old_cart field)
            current_user.update(old_cart="")

        else:
            #Not logged in? create order without user
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            # Get the order ID
            order_id = create_order.pk
            
            # Get product Info
            for product in cart_products():
                # Get product ID
                product_id = product.id
                # Get product price
                price = product.price

                # Get quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()
                        
            # Delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]
        messages.success(request, "Đặt hàng thành công")
        return redirect('home')
    else:
        messages.success(request, "Không truy cập được")
        return redirect('home')

def billing_info(request):
    if request.POST:
		# Get the cart
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quantities
        totals = cart.total()
        shipping_form = request.POST

        # Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #Check if logged in 
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'billing_info.html', {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_info": request.POST,
            "shipping_form": shipping_form,
            "billing_form": billing_form
        })
        else:
            #Not logged in
            billing_form = PaymentForm()
            return render(request, 'billing_info.html', {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_info": request.POST,
            "shipping_form": shipping_form,
            "billing_form": billing_form
        })
    else:
        messages.success(request, "Không truy cập được")
        return redirect('fruits')

def shipped_dash(request):
	if request.user.is_authenticated:
		orders = Order.objects.filter(shipped=True, user=request.user)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, "shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Dành cho người dùng có tài khoản")
		return redirect('home')

def not_shipped_dash(request):
	if request.user.is_authenticated:
		orders = Order.objects.filter(shipped=False, user=request.user)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Dành cho người dùng có tài khoản")
		return redirect('home')
    
def orders(request, pk):
	if request.user.is_authenticated:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')
		return render(request, 'orders.html', {
            "order":order, 
            "items":items
        })

	else:
		return redirect('home')
