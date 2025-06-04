from django.contrib import admin

from product.models import Bundle, Category, Order, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at', 'updated_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status')  # Replace 'order_date' with an actual field like 'created_at'
    search_fields = ('user__username',)
    list_filter = ('status',)
    
    
@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme')
    filter_horizontal = ('products',)  
