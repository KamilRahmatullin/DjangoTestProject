import json

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from shop.models import ProductProxy, Category
from .views import *


class CartViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory().get(reverse('cart:cart_view'))
        self.client = Client()
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_view(self):
        response = self.client.get(reverse('cart:cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart_view.html')
        self.assertTemplateUsed(self.client.get(reverse('cart:cart_view')), 'cart/cart_view.html')


class AddViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = ProductProxy.objects.create(
            category=self.category,
            title='Test product',
            slug='test-product',
            brand='Test brand',
            price=100,
        )
        self.factory = RequestFactory().post(reverse('cart:add_to_cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 1,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_add(self):
        request = self.factory
        response = cart_add(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['cart_qty'], 1)
        self.assertEqual(data['product'], 'Test product')


class CartDeleteViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = ProductProxy.objects.create(
            category=self.category,
            title='Test product',
            slug='test-product',
            brand='Test brand',
            price=100,
        )
        self.factory = RequestFactory().post(reverse('cart:add_to_cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 1,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_delete(self):
        request = self.factory
        response = cart_delete(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['cart_qty'], 0)


class CartUpdateViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = ProductProxy.objects.create(
            category=self.category,
            title='Test product',
            slug='test-product',
            brand='Test brand',
            price=10,
        )
        self.factory = RequestFactory().post(reverse('cart:add_to_cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2,
        })
        self.factory = RequestFactory().post(reverse('cart:update_to_cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 5,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_update(self):
        request = self.factory
        response = cart_add(request)
        response = cart_update(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['cart_total'], '50.00')
        self.assertEqual(data['cart_qty'], 5)
