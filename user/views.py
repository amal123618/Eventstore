
from datetime import timezone
from eventmanagement.models import Event
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import  login, logout as auth_logout
from product.models import Bundle, Order, OrderItem, Product
from user.forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Sum

User = get_user_model()
# Create your views here.

def home(request):
    trending_products = Product.objects.filter(is_trending=True)

    # Group products by 4 for the carousel
    def chunked(iterable, n):
        return [iterable[i:i+n] for i in range(0, len(iterable), n)]

    product_groups = chunked(list(trending_products), 4)
    
    bundles = Bundle.objects.all()
    
    upcoming_event = Event.objects.filter(event_date__gte=now()).order_by('event_date').first()

    if upcoming_event:
        # Calculate the remaining time until the event
        time_remaining = upcoming_event.event_date - now()

        # Convert time remaining to days, hours, minutes, and seconds
        days_left = time_remaining.days
        hours_left = time_remaining.seconds // 3600
        minutes_left = (time_remaining.seconds % 3600) // 60
        seconds_left = time_remaining.seconds % 60
    else:
        days_left = hours_left = minutes_left = seconds_left = 0

    return render(request, 'index.html', {
        'product_groups': product_groups,
        'bundles': bundles,
        'upcoming_event': upcoming_event,
        'days_left': days_left,
        'hours_left': hours_left,
        'minutes_left': minutes_left,
        'seconds_left': seconds_left,
    })

#register
def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
                user = form.save()  
                login(request, user) 
                messages.success(request, "Registration successful!")
                return redirect('login') 
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})

#login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
    return render(request, 'user/login.html')
#logout
def user_logout(request):
    auth_logout(request)
    return redirect('login')

#profile

def profile_view(request):
    user = request.user

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()

        if name:
            name_parts = name.split(" ", 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        user.email = email
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'user/profile.html', {'user': user})




# def admin_dashboard(request):
#     # Get statistics for the dashboard
#     total_sales = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
#     total_orders = Order.objects.count()
#     total_products = Product.objects.count()
#     total_users = User.objects.count()

#     # Example data for graph (you can replace it with real data)
#     order_stats = Order.objects.values('created_at__date').annotate(total=Sum('total_price'))

#     # Render the dashboard template
#     return render(request, 'admin.html', {
#         'total_sales': total_sales,
#         'total_orders': total_orders,
#         'total_products': total_products,
#         'total_users': total_users,
#         'order_stats': order_stats,
#     })




def bundle_view(request, bundle_id):
    bundle = Bundle.objects.get(id=bundle_id)
    products = bundle.products.all()
    return render(request, 'bundle.html', {'bundle': bundle, 'products': products})

def add_bundle_to_cart(request, bundle_id):
    bundle = get_object_or_404(Bundle, id=bundle_id)
    cart = request.session.get('cart', {})

    for product in bundle.products.all():
        product_id = str(product.id)
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1

    request.session['cart'] = cart
    messages.success(request, f"All products in '{bundle.name}' added to cart.")
    return redirect('bundle_detail',{'bundle':bundle})


def vendor_dashboard(request):
    products = Product.objects.filter(vendor=request.user)
    orders = OrderItem.objects.filter(product__vendor=request.user)
    sales_summary = orders.aggregate(total_sales=Sum('price'), items_sold=Sum('quantity'))

    return render(request, 'vendor.html', {
        'products': products,
        'orders': orders,
        'sales_summary': sales_summary
    })