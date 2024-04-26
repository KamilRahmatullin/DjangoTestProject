import string
import random

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def rand_slug():
    """
    Generate a random slug for a category or product.

    Returns:
    str: A randomly generated slug consisting of lowercase letters and digits.
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Категория')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, related_name='children', null=True
    )
    slug = models.SlugField(max_length=200, unique=True, null=False, editable=True, verbose_name='Ссылка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

        # prevent duplicate keys in database
        unique_together = ('slug', 'parent')

    def __str__(self):
        """
        Return a string representation of the Category instance.
        """
        full_path = [self.name]
        k = self.parent
        # print all the ancestors of the category
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        """
        Save method for the Category model.

        If the slug is not specified, it creates a slug from the name using a random string and the name.
        """
        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)

        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_list', args=(self.slug,))


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products',
                                 verbose_name='Категория')
    title = models.CharField(max_length=200, verbose_name='Название товара')
    brand = models.CharField(max_length=200, verbose_name='Бренд')
    description = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(max_length=200, unique=True, null=False, editable=True, verbose_name='Ссылка')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/products/%Y/%m/%d', blank=True, verbose_name='Изображение')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=(self.slug,))


class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Returns a queryset containing only the available products.

        Parameters:
        self: ProductManager instance

        Returns:
        queryset: A queryset containing only the available products.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    objects = ProductManager()

    class Meta:
        proxy = True
