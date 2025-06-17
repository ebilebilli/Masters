from rest_framework import serializers

from services.models.category_model import Category
from services.models.service_model import Service
from core.models.city_model import City
from core.models.language_model import Language
from users.models import CustomUser
from users.models import  WorkImage

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField()
    profession_speciality = serializers.StringRelatedField()
    profession_area = serializers.StringRelatedField()
    languages = serializers.StringRelatedField(many=True)
    cities = serializers.StringRelatedField(many=True)
    work_images = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'profile_image',
            'note',
            'mobile_number',
            'facebook',
            'instagram',
            'tiktok',
            'linkedin',
            'profession_speciality',
            'profession_area',
            'education',
            'education_speciality',
            'languages',
            'cities',
            'work_images',

            'average_rating',
            'average_responsible',
            'average_neat',
            'average_time_management',
            'average_communicative',
            'average_punctual',
            'average_professional',
            'average_experienced',
            'average_efficient',
            'average_agile',
            'average_patient',
            'review_count',
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value not in [None, '', [], {}]}

    


class ProfileUpdateSerializer(serializers.ModelSerializer):
    profession_area = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    profession_speciality = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), required=False)
    cities = serializers.PrimaryKeyRelatedField(many=True, queryset=City.objects.all(), required=False)
    languages = serializers.PrimaryKeyRelatedField(many=True, queryset=Language.objects.all(), required=False)
    profile_image = serializers.ImageField(required=False)


    class Meta:
        model = CustomUser
        fields = [
            "first_name", "last_name", "birth_date", "gender", "mobile_number",
            "profession_area", "profession_speciality", "custom_profession", "experience_years",
            "cities", "education", "education_speciality", "languages",
            "profile_image", "facebook", "instagram", "tiktok", "linkedin", "note"
        ]

    def validate_mobile_number(self, value):
        user = self.instance
        if CustomUser.objects.exclude(pk=user.pk).filter(mobile_number=value).exists():
            raise serializers.ValidationError("Bu mobil nömrə ilə artıq qeydiyyat aparılıb.")
        if not value.isdigit():
            raise serializers.ValidationError("Mobil nömrə yalnız rəqəmlərdən ibarət olmalıdır.")
        if len(value) != 9:
            raise serializers.ValidationError("Mobil nömrə 9 rəqəmdən ibarət olmalıdır.")
        return value

    def validate(self, attrs):
        user = self.instance
        profession_area = attrs.get("profession_area", user.profession_area)
        profession_speciality = attrs.get("profession_speciality", user.profession_speciality)
        custom_profession = attrs.get("custom_profession", user.custom_profession)

        if profession_area and profession_speciality:
            if profession_speciality.category_id != profession_area.id:
                raise serializers.ValidationError({
                    "profession_speciality": "Seçilmiş peşə ixtisası bu sahəyə aid deyil."
                })

        if profession_area.name.lower() == "other":
            if profession_speciality:
                raise serializers.ValidationError({
                    "profession_speciality": "Bu sahə seçiləndə profession_speciality boş olmalıdır."
                })
            if not custom_profession:
                raise serializers.ValidationError({
                    "custom_profession": "Bu sahə seçiləndə custom_profession mütləq doldurulmalıdır."
                })
        else:
            if not profession_speciality:
                raise serializers.ValidationError({
                    "profession_speciality": "Bu sahə üçün profession_speciality vacibdir."
                })
            if custom_profession:
                raise serializers.ValidationError({
                    "custom_profession": "Bu sahə üçün custom_profession boş qalmalıdır."
                })

        education = attrs.get("education", user.education)
        education_speciality = attrs.get("education_speciality", user.education_speciality)
        if education == "0" and education_speciality:
            raise serializers.ValidationError({
                "education_speciality": "Təhsil yoxdursa, ixtisas qeyd edilməməlidir."
            })
        if education != "0" and not education_speciality:
            raise serializers.ValidationError({
                "education_speciality": "Bu sahə mütləq doldurulmalıdır."
            })

        return attrs

    def update(self, instance, validated_data):
        cities = validated_data.pop("cities", None)
        languages = validated_data.pop("languages", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cities is not None:
            instance.cities.set(cities)
        if languages is not None:
            instance.languages.set(languages)

        instance.save()
        return instance