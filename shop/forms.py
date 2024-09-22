from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Review, Order, Product

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'postal_code']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image']


class CheckoutForm(forms.Form):
    address = forms.CharField(
    max_length=255,
    widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your address'}),
    required=True
)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    country = forms.CharField(max_length=100)    
   
    
    payment_method = forms.ChoiceField(
        choices=[
            ('credit_card', 'Credit Card'),
            ('paypal', 'PayPal')
        ],
        required=True
    )
    credit_card_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your credit card number'}),
        required=False
    )
    expiration_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}),
        required=False
    )
    cvv = forms.CharField(
        max_length=3,
        widget=forms.PasswordInput(attrs={'placeholder': 'CVV'}),
        required=False
    )

