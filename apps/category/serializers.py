from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['pk'] = instance.pk

        return rep