from django.urls import path
from . import views

urlpatterns = [
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/update/<int:product_id>/', views.product_update, name='product_update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('category/<str:event_type>/', views.category_products, name='category'),
    
    
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    
    
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),
    
    path('orders/', views.user_orders, name='user_orders'),
    path('order/<int:order_id>/',views.order_details, name='order_details'),
    
   
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    path('products/<int:bundle_id>/', views.product_list, name='product_list'),

    
    
   
    
  

    
    
    

   
]