
from django.db import models

from store import settings
from user.models import User




# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_trending = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.product.name}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') 
    
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def total_items(self):
            return self.cartitem_set.count()

    @property
    def total_price(self):
            return sum(item.total_price for item in self.cartitem_set.all())
        
    @property
    def total_mrp(self):
        return sum(item.product.price * item.quantity for item in self.cartitem_set.all())

    
    @property
    def total_price(self):
        return self.total_mrp 
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    




class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES)  # e.g., Pending, Shipped, Delivered
    updated_at = models.DateTimeField(auto_now=True)

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')

    def __str__(self):
        return f"Shipping Address for Order {self.order.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    
    @property
    def total_price(self):
        return self.product.price * self.quantity


class Bundle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    theme = models.CharField(max_length=100)  # For example: "Wedding", "Christmas"
    products = models.ManyToManyField(Product)
    image = models.ImageField(upload_to='bundle_images/')

    def __str__(self):
        return self.name
    
