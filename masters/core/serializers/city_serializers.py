from rest_framework import serializers
from core.models.city_model import City


class CitySerializer(serializers.ModelSerializer):  
    class Meta:
        model = City
        fields = ['id', 'display_name']


# class DistrictSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = District
#         fields = ['id', 'name', 'display_name', 'city']