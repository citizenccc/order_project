import django_filters
from django_filters.rest_framework import FilterSet

from .models import Order


class OrderFilter(FilterSet):
    start_date = django_filters.DateTimeFilter(lookup_expr="gte", field_name='created_at')
    end_date = django_filters.DateTimeFilter(lookup_expr="lte", field_name='created_at')

    class Meta:
        model = Order
        fields = ('start_date', 'end_date', 'created_at')
