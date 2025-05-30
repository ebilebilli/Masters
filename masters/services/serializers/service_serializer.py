from rest_framework import serializers

from services.models.service_model import Service
from services.models.category_model import Category
from core.models.city_model import City
from .service_image_serializer import ServiceImageSerializer


class ServiceSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
    many=True,
    queryset=Category.objects.all(),
    slug_field='name'
    )
    city = serializers.SlugRelatedField(
    queryset=City.objects.all(),
    slug_field='name'
    )
    image = ServiceImageSerializer(
        many=True,
        read_only=True,
        source='images'
    )

    class Meta:
        model = Service
        fields = '__all__'