from rest_framework import serializers

from core.models.city_model import City
from core.models.language_model import Language
from users.models import CustomUser
from users.models import  WorkImage

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value not in [None, '', [], {}]}
    


# class ProfileUpdateSerializer(serializers.ModelSerializer):
#     cities = serializers.PrimaryKeyRelatedField(many=True, queryset=City.objects.all(), required=False)
#     districts = serializers.PrimaryKeyRelatedField(many=True, queryset=District.objects.all(), required=False)
#     languages = serializers.PrimaryKeyRelatedField(many=True, queryset=Language.objects.all(), required=False)

#     class Meta:
#         model = CustomUser
#         fields = [
#             "first_name", "last_name", "birth_date", "gender", "mobile_number",
#             "profession_area", "profession_speciality", "custom_profession", "experience_years",
#             "cities", "districts", "education", "education_speciality",
#             "languages", "profile_image", "facebook", "instagram", "tiktok", "linkedin", "note"
#         ]

#     def validate_mobile_number(self, value):
#         user = self.instance
#         if CustomUser.objects.exclude(pk=user.pk).filter(mobile_number=value).exists():
#             raise serializers.ValidationError("Bu mobil nömrə ilə artıq qeydiyyat aparılıb.")
#         if not value.isdigit():
#             raise serializers.ValidationError("Mobil nömrə yalnız rəqəmlərdən ibarət olmalıdır.")
#         if len(value) != 9:
#             raise serializers.ValidationError("Mobil nömrə 9 rəqəmdən ibarət olmalıdır.")
#         return value

#     def validate(self, attrs):
#         user = self.instance
#         profession_area = attrs.get("profession_area", user.profession_area)
#         profession_speciality = attrs.get("profession_speciality", user.profession_speciality)
#         custom_profession = attrs.get("custom_profession", user.custom_profession)

#         if profession_area.name.lower() == "other":
#             if profession_speciality:
#                 raise serializers.ValidationError({
#                     "profession_speciality": "Bu sahə seçiləndə profession_speciality boş olmalıdır."
#                 })
#             if not custom_profession:
#                 raise serializers.ValidationError({
#                     "custom_profession": "Bu sahə seçiləndə custom_profession mütləq doldurulmalıdır."
#                 })
#         else:
#             if not profession_speciality:
#                 raise serializers.ValidationError({
#                     "profession_speciality": "Bu sahə üçün profession_speciality vacibdir."
#                 })
#             if custom_profession:
#                 raise serializers.ValidationError({
#                     "custom_profession": "Bu sahə üçün custom_profession boş qalmalıdır."
#                 })

#         education = attrs.get("education", user.education)
#         education_speciality = attrs.get("education_speciality", user.education_speciality)
#         if education == "0" and education_speciality:
#             raise serializers.ValidationError({
#                 "education_speciality": "Təhsil yoxdursa, ixtisas qeyd edilməməlidir."
#             })
#         if education != "0" and not education_speciality:
#             raise serializers.ValidationError({
#                 "education_speciality": "Bu sahə mütləq doldurulmalıdır."
#             })

#         cities = attrs.get("cities", user.cities.all())
#         districts = attrs.get("districts", user.districts.all())

#         if any(city.name.lower() == "baku" for city in cities):
#             if not districts:
#                 raise serializers.ValidationError({
#                     "districts": "Bakı seçildikdə rayonlar mütləq seçilməlidir."
#                 })
#         else:
#             if districts:
#                 raise serializers.ValidationError({
#                     "districts": "Bakı seçilmədikdə rayonlar daxil edilməməlidir."
#                 })

#         return attrs

#     def update(self, instance, validated_data):
#         cities = validated_data.pop("cities", None)
#         districts = validated_data.pop("districts", None)
#         languages = validated_data.pop("languages", None)

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         if cities is not None:
#             instance.cities.set(cities)
#         if districts is not None:
#             instance.districts.set(districts)
#         if languages is not None:
#             instance.languages.set(languages)

#         instance.save()
#         return instance