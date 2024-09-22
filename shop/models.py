from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images/')
    
    # Yeni ve Öne Çıkan Alanları
    is_new = models.BooleanField(default=False)  # Yeni ürün olup olmadığını belirler
    is_featured = models.BooleanField(default=False)  # Öne çıkan ürün olup olmadığını belirler
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)
    
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def get_total_price(self):
        total = sum(item.get_total_item_price() for item in self.cartitem_set.all())
        return total

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)  # Yeni eklenen alan
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def get_total_item_price(self):
        return self.quantity * self.product.price
    

