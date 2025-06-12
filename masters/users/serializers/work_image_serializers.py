from rest_framework import serializers

from users.models import  WorkImage



class WorkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False}
        }