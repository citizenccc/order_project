from django.utils import timezone

from django.db import models
from django.contrib.auth import get_user_model
from apps.product.models import Product

User = get_user_model()


class StatusChoices(models.TextChoices):
    new = ('received', 'New')
    on_process = ('in-process', 'In process')
    delivered = ('delivered', 'Delivered')
    deleted = ('deleted', 'Deleted')
    canceled = ('cancelled', 'Cancelled')


class PaymentChoices(models.TextChoices):
    by_cash = ('cash', 'Card')
    handling_company = ('Credit card', 'Debit card')


class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='orders')
    bort_number = models.CharField(max_length=66, blank=True)
    product = models.ManyToManyField(Product, through='OrderItems')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default="received")
    created_at = models.DateTimeField(auto_now_add=True)
    pre_order_date = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True)
    payment = models.CharField(max_length=20, choices=PaymentChoices.choices)

    def __str__(self):
        return f'Order № {self.id} от {self.created_at.strftime("%d-%m-%Y  %H:%M")} order cost: {self.total_sum}'

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = 'order'
        ordering = ['-created_at']


class OrderItems(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product,
                             on_delete=models.CASCADE,
                             related_name='order_items')
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product}'

    class Meta:
        unique_together = ['order', 'product']
        verbose_name_plural = "Product"
        db_table = 'order_items'
