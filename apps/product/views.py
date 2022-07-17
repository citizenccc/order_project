from rest_framework.viewsets import ModelViewSet
from apps.product.filters import ProductFilter
from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ProductFilter
    # search_fields = ['outlet', ]
    # ordering_fields = ['outlet', ]
    

