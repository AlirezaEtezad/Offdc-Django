from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm  # Fixed typo (was `.froms` instead of `.forms`)
from .models import Product, Cart, CartItem, Order, Category

# Create your views here.

app_name = 'shop'


def index(request):
    return render(request, 'index.html')


def product(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)
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

    else:  # No need for `elif request.method == 'GET'`
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('index')


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def add_to_cart(request, product_id: int):
    """Add a product to the cart or update quantity"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity = quantity if created else cart_item.quantity + quantity
    cart_item.save()

    return redirect('cart')


@login_required
def increase_cart(request, product_id):
    """Increase product quantity in the cart"""
    cart_item = get_object_or_404(CartItem, cart__user=request.user, product_id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required
def decrease_cart(request, product_id):
    """Decrease product quantity, remove item if quantity becomes 0"""
    cart_item = get_object_or_404(CartItem, cart__user=request.user, product_id=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove item completely

    return redirect('cart')


@login_required
def cart(request):
    """Display the cart with total price, maintaining order"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).order_by('id')  # Order by ID

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def remove_from_cart(request, product_id: int):
    """Remove a product completely from the cart"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    
    cart_item.delete()  # Remove item completely

    return redirect('cart')


@login_required
def checkout(request):
    """Process checkout and create an order"""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Create an order
    Order.objects.create(user=request.user, total_price=total_price)

    # Clear the cart
    cart_items.delete()
    
    messages.success(request, 'Your order has been placed successfully!')
    return redirect('profile')



def categories(request):
    parent_categories = Category.objects.filter(parent__isnull=True)  # Get only main categories
    return render(request, 'categories.html', {'parent_categories': parent_categories})

def subcategories(request, category_id):
    category = Category.objects.get(id=category_id)
    subcategories = category.subcategories.all()  # Get subcategories
    return render(request, 'subcategories.html', {'category': category, 'subcategories': subcategories})
