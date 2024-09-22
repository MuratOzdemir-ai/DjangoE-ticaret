from django.test import TestCase
from .models import Product, Category

class ProductModelTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(name='Test Product', category=category, price=10.00)

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 10.00)

