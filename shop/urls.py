from django.urls import path
from . import views
from .views import CustomLoginView, add_to_cart

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('order/create/', views.order_create, name='order_create'),
    path('order/<int:order_id>/summary/', views.order_summary, name='order_summary'),
    path('order/history/', views.order_history, name='order_history'),
    path('cart/', views.cart, name='cart'),  # Sadece bir tane yeter
    #path('cart/', views.view_cart, name='view_cart'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('add_product/', views.add_product, name='add_product'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/', views.order_confirmation, name='order_confirmation'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/', views.order_form_view, name='order_form'),
    path('order/success/', views.order_success, name='order_success'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
