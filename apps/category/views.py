from rest_framework.viewsets import ModelViewSet
from apps.category.models import Category
from apps.category.serializers import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    