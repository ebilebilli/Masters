from rest_framework import serializers

from users.models import CustomUser
from users.serializers.work_image_serializers import WorkImageSerializer


class ProfileSerializer(serializers.ModelSerializer):
    cities = serializers.StringRelatedField(many=True)
    languages = serializers.StringRelatedField(many=True)
    work_images = WorkImageSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = [
            # Şəxsi məlumatlar
            'first_name',
            'last_name',
            'birth_date',
            'gender',
            'mobile_number',

            # Peşə məlumatları
            'profession_area',
            'profession_speciality',
            'custom_profession',
            'experience_years',
            'cities',
            'districts',

            # Təhsil məlumatları
            'education',
            'education_speciality',

            # Dillər
            'languages',

            # Profil və sosial media
            'profile_image',
            'facebook',
            'instagram',
            'tiktok',
            'linkedin',

            # İş şəkilləri
            'work_images',

            # Əlavə qeyd
            'note',
        ]
        read_only_fields = fields