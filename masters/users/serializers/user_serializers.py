from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.models.city_model import City, District
from core.models.language_model import Language
from services.models.category_model import Category
import json

from users.models import CustomUser
from users.models import  WorkImage


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = [
            'password', 'is_superuser', 'is_staff', 'user_permissions', 'groups',
            'last_login', 'is_active', 
        ]
   




# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     password2 = serializers.CharField(write_only=True)

#     cities = serializers.PrimaryKeyRelatedField(many=True, queryset=City.objects.all())
#     districts = serializers.PrimaryKeyRelatedField(many=True, queryset=District.objects.all(), required=False)
#     languages = serializers.PrimaryKeyRelatedField(many=True, queryset=Language.objects.all())

#     work_images = serializers.ListField(
#         child=serializers.ImageField(),
#         write_only=True,
#         required=False
#     )

#     class Meta:
#         model = CustomUser
#         fields = [
#             # Şəxsi məlumatlar
#             'first_name',
#             'last_name',
#             'birth_date',
#             'gender',
#             'mobile_number',

#             # Şifrə
#             'password',
#             'password2',

#             # Peşə məlumatları
#             'profession_area',
#             'profession_speciality',
#             'custom_profession',
#             'experience_years',
#             'cities',
#             'districts',

#             # Təhsil məlumatları
#             'education',
#             'education_speciality',

#             # Dillər
#             'languages',

#             # Profil və sosial media
#             'profile_image',
#             'facebook',
#             'instagram',
#             'tiktok',
#             'linkedin',

#             # İş şəkilləri
#             'work_images',

#             # Əlavə qeyd
#             'note',
#         ]

#     def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)

        # request_data = self.initial_data if hasattr(self, 'initial_data') else {}

        # profession_area = request_data.get("profession_area")
        
        # if profession_area is not None and type(profession_area) == int:
        #     profession_area_name = Category.objects.filter(id=profession_area).first()
        #     if profession_area_name is not None and str(profession_area_name) == "other":
        #         self.fields['profession_speciality'].required = False
        #         self.fields['custom_profession'].required = True
        #     else:
        #         self.fields['profession_speciality'].required = True
        #         self.fields['custom_profession'].required = False

        # # Təhsil üçün
        # education = request_data.get("education")

        # if education == "0":  # "Yoxdur"
        #     self.fields["education_speciality"].required = False
        # else:
        #     self.fields["education_speciality"].required = True

        # # Şəhər üçün
        # city_ids = request_data.get("cities", [])

        # if city_ids is not None and type(city_ids) == int:
        #     if isinstance(city_ids, (str, int)):
        #         city_ids = [int(city_ids)]
        #     elif isinstance(city_ids, list):
        #         city_ids = [int(c) if isinstance(c, str) else c for c in city_ids]
        #     else:
        #         city_ids = []

        #     city_names = City.objects.filter(id__in=city_ids).values_list("name", flat=True)
        #     city_names = [name.lower() for name in city_names]

        #     if "baku" in city_names:
        #         self.fields['districts'].required = True
        #     else:
        #         self.fields['districts'].required = False


#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Şifrələr uyğun deyil."})

#         profession_area = attrs.get('profession_area')
#         profession_speciality = attrs.get('profession_speciality')
#         custom_profession = attrs.get('custom_profession')

#         area_name = getattr(profession_area, 'name', profession_area)
#         if area_name == 'other':
#             if profession_speciality is not None:
#                 raise serializers.ValidationError({
#                     'profession_speciality': 'Bu sahə seçiləndə profession_speciality boş olmalıdır.'
#                 })
#             if not custom_profession:
#                 raise serializers.ValidationError({
#                     'custom_profession': 'Bu sahə seçiləndə custom_profession mütləq doldurulmalıdır.'
#                 })
#         else:
#             if not profession_speciality:
#                 raise serializers.ValidationError({
#                     'profession_speciality': 'Bu sahə üçün profession_speciality vacibdir.'
#                 })
#             if custom_profession:
#                 raise serializers.ValidationError({
#                     'custom_profession': 'Bu sahə üçün custom_profession boş qalmalıdır.'
#                 })
        
#         # Təhsil üçün yoxlanış
#         education = attrs.get("education")
#         speciality = attrs.get("education_speciality")

#         if education == "0" and speciality:
#             raise serializers.ValidationError({
#                 "education_speciality": "Təhsil yoxdursa, ixtisas qeyd edilməməlidir."
#             })

#         if education != "0" and not speciality:
#             raise serializers.ValidationError({
#                 "education_speciality": "Bu sahə mütləq doldurulmalıdır."
#             })

#         # Bakı şəhəri seçilibsə, rayonlar mütləqdir
#         cities = attrs.get('cities', [])
#         districts = attrs.get('districts', [])
#         city_name = [getattr(c, 'name', c) for c in cities]

#         if 'baku' in city_name:
#             if not districts:
#                 raise serializers.ValidationError({
#                     'districts': 'Bakı seçildikdə rayonlar mütləq seçilməlidir.'
#                 })
#         else:
#             if districts:
#                 raise serializers.ValidationError({
#                     'districts': 'Bakı şəhəri seçilmədiyi halda rayonlar daxil edilməməlidir.'
#                 })

#         return attrs

#     def create(self, validated_data):
#         work_images_data = validated_data.pop('work_images', [])
#         password = validated_data.pop('password')
#         validated_data.pop('password2')

#         cities = validated_data.pop('cities', [])
#         districts = validated_data.pop('districts', [])
#         languages = validated_data.pop('languages', [])

#         user = CustomUser.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()

#         def extract_ids(qs):
#             return [obj if isinstance(obj, int) else obj.id for obj in qs]

#         user.cities.set(extract_ids(cities))
#         user.districts.set(extract_ids(districts))
#         user.languages.set(extract_ids(languages))

#         for image in work_images_data:
#             img = WorkImage.objects.create(image=image)
#             user.work_images.add(img)

#         return user


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    cities = serializers.PrimaryKeyRelatedField(many=True, queryset=City.objects.all())
    districts = serializers.PrimaryKeyRelatedField(many=True, queryset=District.objects.all(), required=False)
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
            'districts': {
                'invalid': {'message': 'Rayonlar üçün düzgün ID dəyərləri daxil edin.'}
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

        profession_area = request_data.get("profession_area")
        
        if profession_area is not None and type(profession_area) == int:
            profession_area_name = Category.objects.filter(id=profession_area).first()
            if profession_area_name is not None and str(profession_area_name) == "other":
                self.fields['profession_speciality'].required = False
                self.fields['custom_profession'].required = True
            else:
                self.fields['profession_speciality'].required = True
                self.fields['custom_profession'].required = False

        # Təhsil üçün
        education = request_data.get("education")

        if education == "0":  # "Yoxdur"
            self.fields["education_speciality"].required = False
        else:
            self.fields["education_speciality"].required = True

        # Şəhər üçün
        city_ids = request_data.get("cities", [])

        if city_ids is not None and type(city_ids) == int:
            if isinstance(city_ids, (str, int)):
                city_ids = [int(city_ids)]
            elif isinstance(city_ids, list):
                city_ids = [int(c) if isinstance(c, str) else c for c in city_ids]
            else:
                city_ids = []

            city_names = City.objects.filter(id__in=city_ids).values_list("name", flat=True)
            city_names = [name.lower() for name in city_names]

            if "baku" in city_names:
                self.fields['districts'].required = True
            else:
                self.fields['districts'].required = False

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

    def validate_profession_speciality(self, value):
        area_id = self.initial_data.get('profession_area')
        try:
            area_id = int(area_id)
        except (TypeError, ValueError):
            area_id = None

        if area_id and area_id != 1 and not value:
            raise serializers.ValidationError("Bu peşə sahəsi üçün ixtisas mütləqdir.")
        if area_id == 1 and value:
            raise serializers.ValidationError("Bu peşə sahəsində ixtisas seçilməməlidir.")
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

        profession_area = attrs.get('profession_area')
        profession_speciality = attrs.get('profession_speciality')
        custom_profession = attrs.get('custom_profession')

        area_name = getattr(profession_area, 'name', profession_area)
        if area_name == 'other':
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
        
        # Təhsil üçün yoxlanış
        education = attrs.get("education")
        speciality = attrs.get("education_speciality")

        if education == "0" and speciality:
            raise serializers.ValidationError({
                "education_speciality": "Təhsil yoxdursa, ixtisas qeyd edilməməlidir."
            })

        if education != "0" and not speciality:
            raise serializers.ValidationError({
                "education_speciality": "Bu sahə mütləq doldurulmalıdır."
            })

        # Bakı şəhəri seçilibsə, rayonlar mütləqdir
        cities = attrs.get('cities', [])
        districts = attrs.get('districts', [])
        city_name = [getattr(c, 'name', c) for c in cities]

        if 'baku' in city_name:
            if not districts:
                raise serializers.ValidationError({
                    'districts': 'Bakı seçildikdə rayonlar mütləq seçilməlidir.'
                })
        else:
            if districts:
                raise serializers.ValidationError({
                    'districts': 'Bakı şəhəri seçilmədiyi halda rayonlar daxil edilməməlidir.'
                })

        return attrs

    def create(self, validated_data):
        work_images_data = validated_data.pop('work_images', [])
        password = validated_data.pop('password')
        validated_data.pop('password2')

        cities = validated_data.pop('cities', [])
        districts = validated_data.pop('districts', [])
        languages = validated_data.pop('languages', [])

        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        def extract_ids(qs):
            return [obj if isinstance(obj, int) else obj.id for obj in qs]

        user.cities.set(extract_ids(cities))
        user.districts.set(extract_ids(districts))
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
