from django.db import models
from apps.outlet.models import Outlet
from apps.category.models import Category


class Product(models.Model):
    # outlet = models.ForeignKey(Outlet, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=255)
    description = models.TextField('Description')
    weight = models.CharField('Weight', max_length=20)
    price = models.CharField('Price', max_length=20)
    quantity = models.IntegerField('Quantity')
    img = models.ImageField('Photo', upload_to='product_images', null=True, blank=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)
    image = models.ImageField('Photo', upload_to='product_images', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Product photo'