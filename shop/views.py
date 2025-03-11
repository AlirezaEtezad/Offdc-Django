from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from . import views
from .froms import SignUpForm, SignInForm
from .models import Product, Cart, CartItem, Order

# Create your views here.

app_name = 'shop'

def index(request):
    return render(request, 'index.html')

def product(request, product_id: int):
    product = Product.objects.get(id=product_id)
    return render(request, 'product.html', {'product': product})

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'signup.html', {'form': form})


    elif request.method == 'GET':
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})



# def signin(request):
#     if request.method == 'POST':
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('profile')

#     else:
#         form = SignInForm()
#     return render(request, 'signin.html', {'form': form})

# def signin(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)  # ✅ Use `data=request.POST`
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)  # ✅ Authenticate
#             if user is not None:
#                 login(request, user)
#                 return redirect('profile')
#     else:
#         form = SignInForm()
#     return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('index')


def profile(request):
    return render(request, 'profile.html', {'user': request.user})



@login_required
def add_to_cart(request, product_id: int):
    product = Product.objects.get(id=product_id)

    # Get the quantity from the form submission
    quantity = int(request.POST.get('quantity', 1))

    # Check if the cart exists for the current user, if not, create one
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Update the quantity of the cart item
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart')



@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def remove_from_cart(request, product_id: int):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # Reduce quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove item completely if only 1 left

    return redirect('cart')


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Create an order
    order = Order.objects.create(user=request.user, total_price=total_price)
    order.total_price = sum(item.product.price * item.quantity for item in cart_items)
    # clear order after checkout
    cart_items.delete()
    messages.success(request, 'Your order has been placed successfully!')

    return redirect('profile')