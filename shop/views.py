import paypalrestsdk 
import stripe
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProductForm, ReviewForm, OrderForm, CheckoutForm
from .models import Product, Category, Order, OrderItem, Review, Cart, CartItem
from .cart import ShoppingCart
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User

class CustomLoginView(LoginView):
    template_name = 'shop/login.html'
    authentication_form = CustomAuthenticationForm

class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
        return render(request, 'registration/signup.html', {'form': form})

@login_required
def home(request):
    new_products = Product.objects.filter(is_new=True)[:6]
    featured_products = Product.objects.filter(is_featured=True)[:6]

    context = {
        'new_products': new_products,
        'featured_products': featured_products
    }

    return render(request, 'shop/home.html', context)

@login_required
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def product_list(request):
    category_slug = request.GET.get('category')
    categories = Category.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    return render(request, 'shop/product_list.html', {'products': products, 'categories': categories})

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items
    }
    return render(request, 'shop/cart.html', context)

@login_required
def cart_add(request, product_id):
    cart = ShoppingCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart is None:
        cart = Cart.objects.create(user=request.user)

    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = sum(item.get_total_item_price() for item in cart_items)  # Her bir ürün için toplam fiyatları topla

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def order_success(request):
    return render(request, 'shop/order_success.html')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'shop/add_review.html', {'form': form, 'product': product})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'shop/product_detail.html', {'product': product, 'reviews': reviews})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop:index')
    else:
        form = ProductForm()

    return render(request, 'shop/add_product.html', {'form': form})

@login_required
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/category_products.html', {'category': category, 'products': products})

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data.get('payment_method')
            if payment_method == 'stripe':
                return process_stripe_payment(request, cart)
            elif payment_method == 'paypal':
                return process_paypal_payment(request, cart)
    else:
        form = CheckoutForm()

    return render(request, 'shop/checkout.html', {'form': form, 'cart': cart})

@login_required
def process_stripe_payment(request, cart):
    total_amount = int(cart.get_total_price() * 100)
    token = request.POST.get('stripeToken')

    try:
        charge = stripe.Charge.create(
            amount=total_amount,
            currency='usd',
            description='E-commerce Purchase',
            source=token
        )
        create_order_from_cart(cart)
        return redirect('order_success')
    except stripe.error.CardError as e:
        return render(request, 'shop/error.html', {'message': str(e)})

@login_required
def process_paypal_payment(request, cart):
    # PayPal ödeme işlemleri burada gerçekleştirilecek
    return redirect('order_confirmation')

@login_required
def create_order_from_cart(cart):
    order = Order.objects.create(user=cart.user)
    for item in cart.cartitem_set.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.price,
            quantity=item.quantity
        )
    cart.cartitem_set.all().delete()

@login_required
def order_confirmation(request):
    return render(request, 'shop/order_confirmation.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})

@login_required
def order_form_view(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        return redirect('cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                postal_code=form.cleaned_data['postal_code'],
                city=form.cleaned_data['city'],
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.price,
                    quantity=item.quantity
                )

            cart.clear()
            return redirect('order_success')
    else:
        form = OrderForm()

    return render(request, 'order_form.html', {'form': form, 'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        return redirect('login')
    return redirect('cart')

@login_required
def some_view(request):
    url = reverse('cart')
    return redirect(url)

@login_required
def form_view(request):
    if request.method == 'POST':
        # form işlemleri
        return redirect(reverse('cart'))
    return render(request, 'shop/form_template.html')

@login_required
def order_create(request):
    # Sipariş oluşturma işlemleri
    pass  # Buraya sipariş oluşturma mantığını ekle

@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_summary.html', {'order': order})

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items})