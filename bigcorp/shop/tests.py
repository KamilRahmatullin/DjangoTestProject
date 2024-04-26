from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import ProductProxy, Category, Product


class ProductViewTestCase(TestCase):
    def test_get_products(self):

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        uploaded = SimpleUploadedFile('test_image.gif', content=small_gif, content_type='image/gif')
        category = Category.objects.create(name='Test category')
        # region Create products
        product1 = Product.objects.create(
            category=category,
            title='Test product1',
            slug='test-product1',
            brand='Test brand',
            description='Test description',
            price=100,
            image=uploaded,
            available=True,
        )
        product2 = Product.objects.create(
            category=category,
            title='Test product2',
            slug='test-product2',
            brand='Test brand',
            description='Test description',
            price=150,
            image=uploaded,
            available=True,
        )
        # endregion
        response = self.client.get(reverse('shop:products'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/products.html')
        self.assertEqual(list(response.context['products']), [product1, product2])
        self.assertContains(response, product1)
        self.assertContains(response, product2)


class ProductDetailViewTestCase(TestCase):
    def test_get_product(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        uploaded = SimpleUploadedFile('test_image.gif', content=small_gif, content_type='image/gif')
        category = Category.objects.create(name='Test category')
        # region Create products
        product1 = Product.objects.create(
            category=category,
            title='Test product1',
            slug='test-product1',
            brand='Test brand',
            description='Test description',
            price=100,
            image=uploaded,
            available=True,
        )
        product2 = Product.objects.create(
            category=category,
            title='Test product2',
            slug='test-product2',
            brand='Test brand',
            description='Test description',
            price=150,
            image=uploaded,
            available=True,
        )
        # endregion
        response = self.client.get(reverse('shop:product_detail', args=(product1.slug,)))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')
        self.assertEqual(response.context['product'], product1)
        self.assertEqual(response.context['product'].slug, product1.slug)


class CategoryListViewTestCase(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile('test_image.gif', content=small_gif, content_type='image/gif')
        self.category1 = Category.objects.create(name='Test category1')
        self.category2 = Category.objects.create(name='Test category2')
        self.product = Product.objects.create(
            category=self.category1,
            title='Test product1',
            slug='test-product1',
            brand='Test brand',
            price=100,
            image=uploaded,
        )

    def test_get_category(self):
        response = self.client.get(reverse('shop:category_list', args=(self.category1.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category'], self.category1)
        self.assertTemplateUsed(response, 'shop/category_list.html')
        self.assertEqual(response.context['products'].first(), self.product)