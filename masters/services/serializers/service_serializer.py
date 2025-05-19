from rest_framework import serializers
from services.models.service_model import Service
from .service_image_serializer import ServiceImageSerializer


class ServiceSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(read_only=True)  
    image = ServiceImageSerializer(many=True, read_only=True, source='images') 

    class Meta:
        model = Service
        fields = '__all__'