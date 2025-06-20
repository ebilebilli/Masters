from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.models.city_model import City
from core.models.language_model import Language
from services.models.category_model import Category

from users.models import CustomUser
from users.models import  WorkImage


class CustomUserSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        exclude = [
            'password', 'is_superuser', 'is_staff', 'user_permissions', 'groups',
            'last_login', 'is_active',
        ]
        
    def get_cities(self, obj):
        return [city.display_name for city in obj.cities.all()]


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

            # İş şəkilləri
            'work_images',

            # Əlavə qeyd
            'note',
        ]

    extra_kwargs = {
            'first_name': {
                'required': {'message': 'Ad sahəsi mütləq doldurulmalıdır.'},
                'blank': {'message': 'Ad sahəsi boş ola bilməz.'},
                'invalid': {'message': 'Ad sahəsi üçün düzgün dəyər daxil edin.'}
            },
            'last_name': {
                'required': {'message': 'Soyad sahəsi mütləq doldurulmalıdır.'},
                'blank': {'message': 'Soyad sahəsi boş ola bilməz.'},
                'invalid': {'message': 'Soyad sahəsi üçün düzgün dəyər daxil edin.'}
            },
            'gender': {
                'required': {'message': 'Cins sahəsi mütləq seçilməlidir.'},
                'invalid_choice': {'message': '"{input}" düzgün seçim deyil.'}
            },
            'mobile_number': {
                'required': {'message': 'Mobil nömrə mütləq daxil edilməlidir.'},
                'unique': {'message': 'Bu mobil nömrə ilə artıq qeydiyyat aparılıb.'},
                'invalid': {'message': 'Mobil nömrə yalnız rəqəmlərdən ibarət olmalıdır.'}
            },
            'profession_area': {
                'required': {'message': 'Peşə sahəsi mütləq seçilməlidir.'},
                'null': {'message': 'Peşə sahəsi boş ola bilməz.'}
            },
            'experience_years': {
                'required': {'message': 'Təcrübə illəri mütləq daxil edilməlidir.'},
                'invalid': {'message': 'İş təcrübəsi üçün düzgün rəqəm daxil edin.'}
            },
            'cities': {
                'required': {'message': 'Ən azı bir şəhər seçilməlidir.'},
                'invalid': {'message': 'Şəhərlər üçün düzgün ID dəyərləri daxil edin.'}
            },
            'languages': {
                'required': {'message': 'Ən azı bir dil seçilməlidir.'},
                'invalid': {'message': 'Dillər üçün düzgün ID dəyərləri daxil edin.'}
            },
            'education': {
                'required': {'message': 'Təhsil sahəsi mütləq seçilməlidir.'},
                'invalid_choice': {'message': 'Təhsil üçün düzgün seçim daxil edin.'}
            },
            'education_speciality': {
                'required': {'message': 'Təhsil ixtisası mütləq daxil edilməlidir.'},
                'invalid': {'message': 'Təhsil ixtisası yalnız hərflərdən ibarət olmalıdır.'}
            },
            'custom_profession': {
                'invalid': {'message': 'Xüsusi ixtisas sahəsi yalnız hərflərdən ibarət olmalıdır.'}
            }
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request_data = self.initial_data if hasattr(self, 'initial_data') else {}

        profession_speciality = request_data.get("profession_speciality")
        
        if profession_speciality is not None and type(profession_speciality) == int:
            profession_speciality_name = Category.objects.filter(id=profession_speciality).first()
            if profession_speciality_name is not None and str(profession_speciality_name) == "other":
                self.fields['custom_profession'].required = True
            else:
                self.fields['custom_profession'].required = False

        # Təhsil üçün
        education = request_data.get("education")

        if education == "0":  # "Yoxdur"
            self.fields["education_speciality"].required = False
        else:
            self.fields["education_speciality"].required = True

    def validate_mobile_number(self, value):
        if CustomUser.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Bu mobil nömrə ilə artıq qeydiyyat aparılıb.")
        if not value.isdigit():
            raise serializers.ValidationError("Mobil nömrə yalnız rəqəmlərdən ibarət olmalıdır.")
        if len(value) != 9:
            raise serializers.ValidationError("Mobil nömrə 9 rəqəmdən ibarət olmalıdır.")
        return value

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Ad sahəsi boş ola bilməz.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Ad ən azı 2 simvol olmalıdır.")
        return value    


    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Soyad sahəsi boş ola bilməz.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Soyad ən azı 2 simvol olmalıdır.")
        return value


    def validate_education_speciality(self, value):
        if value and any(char.isdigit() for char in value):
            raise serializers.ValidationError("Təhsil üzrə ixtisas yalnız hərflərdən ibarət olmalıdır.")
        return value

    def validate_birth_date(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Doğum tarixi indiki tarixdən sonrakı bir tarix ola bilməz.")
        return value

    def validate_experience_years(self, value):
        if value > 100:
            raise serializers.ValidationError("İş təcrübəsi 100 ildən çox ola bilməz.")
        return value

    def validate_custom_profession(self, value):
        if value and not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError("Xüsusi ixtisas sahəsi yalnız hərflərdən ibarət olmalıdır.")
        if value and len(value.strip()) < 3:
            raise serializers.ValidationError("Xüsusi ixtisas sahəsi ən azı 3 simvol olmalıdır.")
        return value

    def validate_profession_area(self, value):
        if not value:
            raise serializers.ValidationError("Peşə sahəsi mütləq seçilməlidir.")
        return value
    
    def validate_languages(self, value):
        if not value:
            raise serializers.ValidationError("Ən azı bir dil seçilməlidir.")
        return value

    def validate_cities(self, value):
        if not value:
            raise serializers.ValidationError("Ən azı bir şəhər seçilməlidir.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Şifrələr uyğun deyil."})

        profession_speciality = attrs.get('profession_speciality')
        custom_profession = attrs.get('custom_profession')

        speciality_name = getattr(profession_speciality, 'name', profession_speciality)
        if speciality_name == 'other':
            if not custom_profession:
                raise serializers.ValidationError({
                    'custom_profession': f"Peşə ixtisası 'digər' seçiləndə custom_profession mütləq doldurulmalıdır."
                })
        else:
            if not profession_speciality:
                raise serializers.ValidationError({
                    'profession_speciality': 'Peşə ixtisası qeyd etmək vacibdir.'
                })
            if custom_profession:
                raise serializers.ValidationError({
                    'custom_profession': 'Bu sahə boş qalmalıdır.'
                })
        
        # Təhsil üçün yoxlanış
        education = attrs.get("education")
        speciality = attrs.get("education_speciality")

        if education != "0" and not speciality:
            raise serializers.ValidationError({
                "education_speciality": "Bu sahə mütləq doldurulmalıdır."
            })

        return attrs

    def create(self, validated_data):
        work_images_data = validated_data.pop('work_images', [])
        password = validated_data.pop('password')
        validated_data.pop('password2')

        first_name = validated_data.pop('first_name', '').capitalize()
        last_name = validated_data.pop('last_name', '').capitalize()

        education_speciality = validated_data.pop('education_speciality', '')
        if education_speciality:
            education_speciality = education_speciality.capitalize()

        cities = validated_data.pop('cities', [])
        languages = validated_data.pop('languages', [])

        user = CustomUser.objects.create(
            **validated_data,
            first_name = first_name,
            last_name = last_name,
            education_speciality = education_speciality,
        )
        user.set_password(password)
        user.save()

        def extract_ids(qs):
            return [obj if isinstance(obj, int) else obj.id for obj in qs]

        user.cities.set(extract_ids(cities))
        user.languages.set(extract_ids(languages))

        for image in work_images_data:
            img = WorkImage.objects.create(image=image)
            user.work_images.add(img)

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