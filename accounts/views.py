from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateProfileForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib import messages
from .models import Profile
from cart.cart import Cart
import json

# Create your views here.
def profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        return render(request, "acc.html", {
            "username": current_user.username,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "email": current_user.email
        })
    else:
        return redirect('home')

def login_user(request):
    if request.user.is_authenticated:
         return redirect('fruits')
    else:     
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                #Cart persistence while logged in 
                current_user = Profile.objects.get(user__id=request.user.id)
                saved_cart = current_user.old_cart
                if saved_cart:
                    #conver old cart which is a string into a dictionary
                    converted_cart = json.loads(saved_cart)
                    cart = Cart(request)
                    for key,value in converted_cart.items():
                        cart.re_add(product=key, quantity=value)

                messages.success(request, ("Đăng nhập thành công"))
                return redirect('profile')
            else:
                messages.success(request, ("Xin vui lòng nhập lại"))
                return redirect('login')
        else:
            return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def signup_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Đăng ký thành công. Xin hãy điền thông tin thanh toán"))
            return redirect('update_info')
        else: 
            messages.success(request, ("Lỗi, xin hãy thử lại"))
            return redirect('signup')
    else:
        return render(request, 'signup.html', {
            "form": form
        })

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateProfileForm(request.POST or None, instance=current_user)     #get original user form
        if user_form.is_valid():
            user_form.save() #save original form
            login(request, current_user)  # Log the user back in to refresh their session with the new data
            messages.success(request, ("Cập nhật thành công"))
            return redirect('profile')  # Redirect to a profile page or any other page
        return render (request, "editacc.html", {
            "user_form": user_form
        })
    else: 
        messages.success(request, "Bạn không có tài khoản")
        return redirect('editacc.html')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Đổi mật khẩu thành công")
                login(request, current_user)
                return redirect('update_user')
            else: 
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {
                'form': form
            })
    else:
        messages.success(request, "Bạn chưa đăng nhập")
        return redirect('home')
    
@login_required
def update_info(request):
    user = request.user
    
    try:
        # Get or create current user's profile
        current_user_profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        current_user_profile = Profile.objects.create(user=user)
    
    shipping_address, created = ShippingAddress.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST, instance=shipping_address)
        
        if shipping_form.is_valid():
            shipping_form.save()
            messages.success(request, "Cập nhật thành công")
            return redirect('profile')
        else:
            messages.error(request, "Có lỗi xảy ra trong quá trình cập nhật.")
    else:
        form = UserInfoForm(instance=current_user_profile)
        shipping_form = ShippingForm(instance=shipping_address)
    
    return render(request, "update_info.html", {
        'form': form,
        'shipping_form': shipping_form
    })
    
# def update_info(request):
# 	if request.user.is_authenticated:
# 		current_user = Profile.objects.get(user__id=request.user.id)# Get Current User
# 		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)# Get Current User's Shipping Info
		
# 		form = UserInfoForm(request.POST or None, instance=current_user)# Get original User Form
# 		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)	# Get User's Shipping Form	
# 		if form.is_valid() or shipping_form.is_valid():
# 			form.save() # Save original form
# 			shipping_form.save() #save shipping form
# 			messages.success(request, "Cập nhật thành công")
# 			return redirect('profile')
# 		return render(request, "update_info.html", {
#             'form':form, 
#             'shipping_form':shipping_form
#         })
# 	else:
# 		messages.success(request, "Bạn chưa đăng nhập")
# 		return redirect('login')
