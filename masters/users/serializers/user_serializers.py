from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.models.city_model import City
from core.models.language_model import Language

from users.models import CustomUser
from users.models import  WorkImage


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = [
            'password', 'is_superuser', 'is_staff', 'user_permissions', 'groups',
            'last_login', 'is_active', 
        ]
   

class WorkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = '__all__'
        extra_kwargs = {
            'image': {'required': False}
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    cities = serializers.PrimaryKeyRelatedField(many=True, queryset=City.objects.all())
    languages = serializers.PrimaryKeyRelatedField(many=True, queryset=Language.objects.all())

    class Meta:
        model = CustomUser
        fields = [
            # Şəxsi məlumatlar
            'first_name',
            'last_name',
            'birth_date',
            'gender',
            'mobile_number',

            # Şifrə
            'password',
            'password2',

            # Peşə məlumatları
            'profession_area',
            'profession_speciality',
            'custom_profession',
            'experience_years',
            'cities',

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

            # İş şəkilləri (yalnız read_only)
            'work_images',

            # Əlavə qeyd
            'note',
        ]
        extra_kwargs = {
            'work_images': {'read_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Şifrələr uyğun deyil."})
        return attrs

    def create(self, validated_data):
        work_images_data = validated_data.pop('work_images', []) 

        password = validated_data.pop('password')
        validated_data.pop('password2')

        cities = validated_data.pop('cities', [])
        languages = validated_data.pop('languages', [])

        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        user.cities.set(cities)
        user.languages.set(languages)

        print(work_images_data)

        for image in work_images_data:
            work_image = WorkImage.objects.create(image=image)
            user.work_images.add(work_image)

        # İş şəkillərini əlavə et (FILES-dən)

        # request = self.context.get('request')
        # if request:
        #     work_images_files = request.FILES.getlist('work_images')
        #     for idx, file in enumerate(work_images_files):
        #         work_image = WorkImage.objects.create(image=file, order=idx)
        #         user.work_images.add(work_image)


        return user



class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        mobile_number = attrs.get("mobile_number")
        password = attrs.get("password")

        if not mobile_number or not password:
            raise serializers.ValidationError("Mobil nömrə və şifrə tələb olunur.")

        user = authenticate(username=mobile_number, password=password)

        if not user:
            raise serializers.ValidationError("Mobil nömrə və ya şifrə yanlışdır.")

        if not user.is_active:
            raise serializers.ValidationError("Bu hesab deaktiv edilib.")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mobile_number": user.mobile_number,
            }
        }



class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        mobile_number = attrs.get("mobile_number")
        password = attrs.get("password")

        if not mobile_number or not password:
            raise serializers.ValidationError("Mobil nömrə və şifrə tələb olunur.")

        user = authenticate(username=mobile_number, password=password)

        if not user:
            raise serializers.ValidationError("Mobil nömrə və ya şifrə yanlışdır.")

        if not user.is_active:
            raise serializers.ValidationError("Bu hesab deaktiv edilib.")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mobile_number": user.mobile_number,
            }
        }



class ProfileUpdateSerializer(serializers.ModelSerializer):
    cities = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), many=True, required=False)
    languages = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), many=True, required=False)
    work_images = serializers.PrimaryKeyRelatedField(queryset=WorkImage.objects.all(), many=True, required=False)

    class Meta:
        model = CustomUser
        exclude = ['password', 'last_login', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        cities = validated_data.pop('cities', None)
        languages = validated_data.pop('languages', None)
        work_images = validated_data.get('work_images', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cities is not None:
            instance.cities.set(cities)
        if languages is not None:
            instance.languages.set(languages)
        if work_images is not None:
            instance.work_images.set(work_images)

        instance.save()
        return instance