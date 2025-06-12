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

    work_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Daxil olunan məlumatlardan profession_area ID-ni götür
        profession_area_id = None
        request_data = self.initial_data if hasattr(self, 'initial_data') else {}

        if request_data.get("profession_area"):
            try:
                profession_area_id = int(request_data.get("profession_area"))
            except ValueError:
                pass

        DEFAULT_AREA_ID = 1  

        if profession_area_id == DEFAULT_AREA_ID:
            self.fields['profession_speciality'].required = False
            self.fields['custom_profession'].required = True
        else:
            self.fields['profession_speciality'].required = True
            self.fields['custom_profession'].required = False

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Şifrələr uyğun deyil."})

        profession_area = attrs.get('profession_area')
        profession_speciality = attrs.get('profession_speciality')
        custom_profession = attrs.get('custom_profession')

        DEFAULT_AREA_ID = 1  

        # profession_area int və ya object ola bilər
        profession_area_id = getattr(profession_area, 'id', profession_area)

        if profession_area_id == DEFAULT_AREA_ID:
            if profession_speciality is not None:
                raise serializers.ValidationError({
                    'profession_speciality': 'Bu sahə seçiləndə profession_speciality boş olmalıdır.'
                })
            if not custom_profession:
                raise serializers.ValidationError({
                    'custom_profession': 'Bu sahə seçiləndə custom_profession mütləq doldurulmalıdır.'
                })
        else:
            if not profession_speciality:
                raise serializers.ValidationError({
                    'profession_speciality': 'Bu sahə üçün profession_speciality vacibdir.'
                })
            if custom_profession:
                raise serializers.ValidationError({
                    'custom_profession': 'Bu sahə üçün custom_profession boş qalmalıdır.'
                })

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

        for image in work_images_data:
            work_image = WorkImage.objects.create(image=image)
            user.work_images.add(work_image)

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