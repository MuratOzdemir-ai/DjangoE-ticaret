from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Review, Cart, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'available', 'image', 'slug')
    list_filter = ('category', 'available')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'created_at', 'paid')
    list_filter = ('paid', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')

