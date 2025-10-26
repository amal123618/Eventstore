
from datetime import timezone
from eventmanagement.models import Event, Guest
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from product.models import Bundle,Product, Order, Cart, CartItem
from user.forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from product.models import Bundle
from product.models import Bundle, Product
from product.views import cart_view
from django.contrib.auth.decorators import login_required

User = get_user_model()
# Create your views here.

@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access the admin dashboard.")
        return redirect('home')

    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_events = Event.objects.count()

    recent_orders = Order.objects.order_by('-created_at')[:5]
    recent_events = Event.objects.order_by('-event_date')[:5]

    from django.db.models import Sum
    revenue_total = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_events': total_events,
        'recent_orders': recent_orders,
        'recent_events': recent_events,
        'revenue_total': revenue_total,
    }
    return render(request, 'admin/dashboard.html', context)
@login_required(login_url='login')
def admin_users(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    UserModel = get_user_model()
    users = UserModel.objects.all().order_by('-date_joined')
    return render(request, 'admin/users.html', {'users': users})

@login_required(login_url='login')
def admin_user_delete(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')
    UserModel = get_user_model()
    if request.user.id == user_id:
        messages.error(request, "You cannot delete your own account.")
        return redirect('admin_users')
    u = get_object_or_404(UserModel, id=user_id)
    u.delete()
    messages.success(request, "User deleted.")
    return redirect('admin_users')

@login_required(login_url='login')
def admin_events(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    events = Event.objects.select_related('user').order_by('-event_date')
    return render(request, 'admin/events.html', {'events': events})

@login_required(login_url='login')
def admin_event_delete(request, event_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')
    e = get_object_or_404(Event, id=event_id)
    e.delete()
    messages.success(request, "Event deleted.")
    return redirect('admin_events')

@login_required(login_url='login')
def admin_guests(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    guests = Guest.objects.select_related('event', 'event__user').order_by('-id')
    return render(request, 'admin/guests.html', {'guests': guests})

@login_required(login_url='login')
def admin_guest_delete(request, guest_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')
    g = get_object_or_404(Guest, id=guest_id)
    g.delete()
    messages.success(request, "Guest deleted.")
    return redirect('admin_guests')

@login_required(login_url='login')
def admin_orders(request):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    status = request.GET.get('status')
    qs = Order.objects.select_related('user').order_by('-created_at')
    if status:
        qs = qs.filter(status=status)
    # Simple pagination could be added later
    return render(request, 'admin/orders.html', {
        'orders': qs,
        'current_status': status or '',
        'status_choices': [s for s, _ in Order.STATUS_CHOICES],
    })

@login_required(login_url='login')
def admin_order_update_status(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('admin_orders')
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    valid_statuses = [s for s, _ in Order.STATUS_CHOICES]
    if new_status not in valid_statuses:
        messages.error(request, "Invalid status value.")
        return redirect('admin_orders')
    order.status = new_status
    order.save()
    messages.success(request, f"Order {order.id} status updated to {new_status}.")
    return redirect('admin_orders')
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
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different one.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered. Try logging in or use another email.")
            else:
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {'form': form})

#login
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password')
    return render(request, 'user/login.html')
#logout
def user_logout(request):
    auth_logout(request)
    return redirect('login')

#profile
@login_required(login_url='login')   
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






def bundle_view(request, bundle_id):
    bundle = Bundle.objects.get(id=bundle_id)
    products = bundle.products.all()
    return render(request, 'bundle.html', {'bundle': bundle, 'products': products})


@login_required(login_url='login')   
def add_bundle_to_cart(request, bundle_id):
    bundle = get_object_or_404(Bundle, id=bundle_id)
    # Use DB-backed cart tied to the logged-in user
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Add each product in the bundle to the cart as a CartItem
    for product in bundle.products.all():
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
        if not created:
            item.quantity += 1
            item.save()

    messages.success(request, f"Bundle '{bundle.name}' and its products were added to your cart.")
    return redirect('cart_view')



