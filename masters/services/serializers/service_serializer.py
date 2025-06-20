from rest_framework import serializers

from services.models.service_model import Service
from .category_serializer import CategorySerializer


class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = Service
        fields = ['id', 'display_name', 'category']

