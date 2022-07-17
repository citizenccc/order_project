from django_filters.rest_framework import FilterSet

from .models import Product


class ProductFilter(FilterSet):

    class Meta:
        model = Product
        # fields = ('outlet',)
        fields = ('id', 'category', 'title', 'description', 'weight', 'price', 'quantity')