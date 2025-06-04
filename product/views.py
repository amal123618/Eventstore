from datetime import datetime, timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import models
from product.forms import ProductForm,CategoryForm, ReviewForm, ShippingAddressForm
from product.models import Bundle, Cart, CartItem, Order, OrderItem, Product,Category, Review, Wishlist
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.paginator import Paginator

User = get_user_model()


def category_create(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form=CategoryForm
    return render(request,'category_form.html')

def category_list(request):
    category=Category.objects.all()
    return render(request,'products/categories.html',{'category':category})

def category_update(request,category_id):
    category=Category.objects.get(id=category_id)
    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save
        else:
            messages.error(request, 'category not found')
    return render(request, 'category_form.html', {'category': category})

def category_delete(request,category_id):
    category=Category.objects.get(id=category_id)
    category.delete()
    return redirect('category_create')

def category_products(request, event_type):

    products = Product.objects.filter(category__name__exact=event_type)

    return render(request, 'products/category_products.html', {'products': products, 'event_type': event_type})

def create_product(request):
    categories=Category.objects.all()
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form=ProductForm()
    return render(request,'addprocut.html',{'categories':categories})

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

 
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

   
    selected_categories = request.GET.getlist('category')

    if selected_categories:
        products = products.filter(category__id__in=selected_categories)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

   
    paginator = Paginator(products, 9)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'selected_categories': selected_categories,
    }
    return render(request, 'products/product_list.html', context)

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            product.rating = Review.objects.filter(product=product).aggregate(models.Avg('rating'))['rating__avg']
            product.review_count = Review.objects.filter(product=product).count()
            product.save()

            messages.success(request, "Review submitted successfully!")
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist_view')


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    if not wishlist_items.exists():
        messages.info(request, "Your wishlist is empty.")
    return render(request, 'products/whishlist.html', {'wishlist_items': wishlist_items})
@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    wishlist_item.delete()
    messages.success(request, "Item removed from your wishlist.")
    return redirect('wishlist_view')


def product_update(request,product_id):
    product=Product.objects.get(id=product_id)
    categories=Category.objects.all()
    if request.method=='POST':
        form=ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        messages.error(request,'product not found')
    return render(request,'product_form.html',{'product':product,'categories':categories})

def product_delete(request,product_id):
    product=Product.objects.get(id=product_id)
    product.delete()
    return redirect('product_list')




def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'products/cart.html', {'cart': cart})

def add_to_cart(request, product_id):
    
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add items to your cart.")
        return redirect('login')  

    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to your cart!")
    return redirect('cart_view')

def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = request.POST.get('quantity', 1)
    
    try:
        quantity = int(quantity)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
    except ValueError:
        pass
    
    return redirect('cart_view')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_view')






def checkout_view(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(user=request.user, total_price=cart.total_price)
    
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.order = order
            shipping.save()

            for item in cart.cartitem_set.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart.cartitem_set.all().delete()  # Clear cart
            order.is_paid = True  # Set to True only after payment in real-world
            order.paid_at = datetime.now(timezone.utc)
            order.save()
            return redirect('order_success', order_id=order.id)
    else:
        form = ShippingAddressForm()

    return render(request, 'products/checkout.html', {'form': form, 'cart': cart})

def order_success_view(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'products/success.html', {'order': order})

def order_details(request, order_id):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to view your order details.")
        return redirect('login')
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    return render(request, 'products/order_detail.html', {
        'order': order
    })
    
def user_orders(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to view your orders.")
        return redirect('login')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'products/user_orders.html', {
        'orders': orders
    })
    
    
# def curated_bundles(request):
    
#     print(bundles) 
#     return render(request, 'index.html', {'bundles': bundles})
    
    
    
    
