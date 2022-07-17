import django_filters
from django_filters.rest_framework import FilterSet

from .models import Outlet


class OutletFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')


    class Meta:
        model = Outlet
        fields = ('title', 'city')