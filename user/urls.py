from django import views
from django.urls import path
from .views import add_bundle_to_cart, bundle_view, home, profile_view, register_user, login_user, user_logout, vendor_dashboard
urlpatterns = [
    path("", home, name="home"),
    path('register/', register_user, name='register'),
    path('login/',login_user, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    # path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('bundle/<int:bundle_id>/', bundle_view, name='bundle_view'),
    path('bundle/<int:bundle_id>/', add_bundle_to_cart, name='add_bundle_to_cart'),
    path('vendor', vendor_dashboard, name='vendor_profile'),
]