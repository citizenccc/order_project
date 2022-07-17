from rest_framework import serializers

from apps.category.serializers import CategorySerializer
from apps.product.models import Product
from .models import Outlet, OutletImage


class OutletImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutletImage
        fields = ('image', )


class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outlet
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = OutletImageSerializer(instance.outlet_images.all(), many=True).data
        names = Product.objects.filter(outlet=instance.id)
        representation['categories'] = []
        for cat_name in names.iterator():
            representation['categories'].append(cat_name.category.name)
        representation['categories'] = list(set(representation['categories']))
        return representation

