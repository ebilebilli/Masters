from rest_framework import serializers

from users.models import CustomUser
from users.serializers.work_image_serializers import WorkImageSerializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value not in [None, '', [], {}]}