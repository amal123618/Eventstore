from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    add_bundle_to_cart,
    admin_dashboard,
    admin_events,
    admin_event_delete,
    admin_guest_delete,
    admin_guests,
    admin_order_update_status,
    admin_orders,
    admin_user_delete,
    admin_users,
    bundle_view,
    home,
    login_user,
    profile_view,
    register_user,
    user_logout,
)

urlpatterns = [
    path("", home, name="home"),
    path('login/', login_user, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('register/', register_user, name='register'),
    path('bundle/<int:bundle_id>/', bundle_view, name='bundle_view'),
    path('bundle/<int:bundle_id>/add/', add_bundle_to_cart, name='add_bundle_to_cart'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/events/', admin_events, name='admin_events'),
    path('dashboard/events/<int:event_id>/delete/', admin_event_delete, name='admin_event_delete'),
    path('dashboard/guests/', admin_guests, name='admin_guests'),
    path('dashboard/guests/<int:guest_id>/delete/', admin_guest_delete, name='admin_guest_delete'),
    path('dashboard/orders/', admin_orders, name='admin_orders'),
    path('dashboard/orders/<int:order_id>/status/', admin_order_update_status, name='admin_order_update_status'),
    path('dashboard/users/', admin_users, name='admin_users'),
    path('dashboard/users/<int:user_id>/delete/', admin_user_delete, name='admin_user_delete'),
    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
]