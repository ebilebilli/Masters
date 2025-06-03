from rest_framework import serializers
from users.models import CustomUser
from core.models import City
from users.models import Language, WorkImage


# class RegisterSerializer(serializers.ModelSerializer):
#     # Əlavə sahələr üçün ID-lər (m2m)
#     cities = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), many=True)
#     languages = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), many=True)
#     work_images = serializers.PrimaryKeyRelatedField(queryset=WorkImage.objects.all(), many=True, required=False)

#     password = serializers.CharField(write_only=True, min_length=8)
#     password2 = serializers.CharField(write_only=True, min_length=8)

#     class Meta:
#         model = CustomUser
#         fields = [
#             'first_name', 'last_name', 'birth_date', 'mobile_number', 'gender',
#             'profession_area', 'profession_speciality', 'experience_years',
#             'cities', 'education', 'education_speciality', 'languages',
#             'profile_image', 'facebook', 'instagram', 'tiktok', 'linkedin',
#             'work_images', 'note',
#             'password', 'password2'
#         ]

#     def validate(self, attrs):
#         if attrs.get('password') != attrs.get('password2'):
#             raise serializers.ValidationError({"password": "Şifrələr uyğun deyil."})
#         return attrs

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         validated_data.pop('password2')

#         cities = validated_data.pop('cities', [])
#         languages = validated_data.pop('languages', [])
#         work_images = validated_data.pop('work_images', [])

#         user = CustomUser.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()

#         user.cities.set(cities)
#         user.languages.set(languages)
#         user.work_images.set(work_images)

#         return user
    


class WorkImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    order = serializers.IntegerField(required=False)


class RegisterSerializer(serializers.ModelSerializer):
    cities = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), many=True)
    languages = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), many=True)
    work_images = WorkImageSerializer(many=True, required=False)

    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'birth_date', 'mobile_number', 'gender',
            'profession_area', 'profession_speciality', 'experience_years',
            'cities', 'education', 'education_speciality', 'languages',
            'profile_image', 'facebook', 'instagram', 'tiktok', 'linkedin',
            'work_images', 'note',
            'password', 'password2'
        ]

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Şifrələr uyğun deyil."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')

        cities = validated_data.pop('cities', [])
        languages = validated_data.pop('languages', [])
        work_images_data = validated_data.pop('work_images', [])

        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        user.cities.set(cities)
        user.languages.set(languages)

        for img_data in work_images_data:
            image = img_data['image']
            order = img_data.get('order', 0)
            work_image = WorkImage.objects.create(image=image, order=order)
            user.work_images.add(work_image)

        return user