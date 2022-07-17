from rest_framework import serializers
from .models import City


class CitySerilizer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('city', )