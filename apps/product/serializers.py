from rest_framework import serializers
from .models import Product
from ..category.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data.get('name')  # getting value from dict
        return representation