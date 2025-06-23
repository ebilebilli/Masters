import re
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.models.city_model import City, District
from core.models.language_model import Language
from services.models.category_model import Category
from services.models.service_model import Service

from users.models import CustomUser
from users.models import  WorkImage


class CustomUserSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()
    districts = serializers.SerializerMethodField()
    profile_image = serializers.ImageField()
    profession_speciality = serializers.StringRelatedField()
    profession_area = serializers.StringRelatedField()
    languages = serializers.StringRelatedField(many=True)
    work_images = serializers.StringRelatedField(many=True)
    class Meta:
        model = CustomUser
        exclude = [
            'password', 'is_superuser', 'is_staff', 'is_master', 'user_permissions', 'groups',
            'last_login', 'is_active',
        ]
        
    def get_cities(self, obj):
        return [city.display_name for city in obj.cities.all()]
    
    def get_districts(self, obj):
        return [district.display_name for district in obj.districts.all()] 
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['education'] = instance.get_education_display()

        data['gender'] = instance.get_gender_display()  

        if instance.profession_area:
            data['profession_area'] = instance.profession_area.display_name

        if instance.profession_speciality:
            data['profession_speciality'] = instance.profession_speciality.display_name

        return {key: value for key, value in data.items() if value not in [None, '', [], {}]}

    def get_languages(self, obj):  
        return [lang.display_name for lang in obj.languages.all()]
    
    def get_profession_area(self, obj):
        return obj.profession_area.name 

    def get_profession_speciality(self, obj):
        return obj.profession_speciality.name
    
    
    def get_average_rating(self, obj):
        return obj.average_rating()



class MobileNumberSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            'blank': "Zəhmət olmasa, məlumatları daxil edin.",
            'required': "Zəhmət olmasa, məlumatları daxil edin."
        }
    )

    def validate_mobile_number(self, value):
        if not value:
            raise serializers.ValidationError("Zəhmət olmasa, məlumatları daxil edin.")

        def check_number(phone):
            flag1 = False
            flag2 = False
            flag3 = False
            print(phone)

            valid_prefixes = ['10', '50', '51', '55', '70', '77', '99']
            prefix = phone[:2]

            if prefix in valid_prefixes:
                flag1 = True

            if phone.isdigit():
                flag2 = True

            if len(phone) == 9:
                flag3 = True

            if flag1 and flag2 and flag3:
                return False
            else:
                return True
            
        if check_number(phone=value):
            raise serializers.ValidationError("Mobil nömrə düzgün daxil edilməyib. 501234567 formatında daxil edin.")

        if CustomUser.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Bu mobil nömrə ilə istifadəçi artıq mövcuddur. Zəhmət olmasa, başqa mobil nömrə daxil edin.")

        return value


class RegisterSerializer(serializers.ModelSerializer):
    work_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    first_name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Zəhmət olmasa, məlumatları daxil edin.",
            "required": "Zəhmət olmasa, məlumatları daxil edin."
        }
    )

    last_name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Zəhmət olmasa, məlumatları daxil edin.",
            "required": "Zəhmət olmasa, məlumatları daxil edin."
        }
    )

    birth_date = serializers.DateField(
        required=False,
        allow_null=True,
        input_formats=["%Y/%m/%d"],
        error_messages={
            "null": "Zəhmət olmasa, məlumatları daxil edin.",
            "invalid": "Doğum tarixi 'YYYY/MM/DD' formatında olmalıdır. Məsələn: 2000/01/30",
            "required": "Zəhmət olmasa, məlumatları daxil edin."
        }
    )

    gender = serializers.ChoiceField(
        choices=[("MALE", "Kişi"), ("FEMALE", "Qadın")],
        error_messages={
            "blank": "Zəhmət olmasa, seçim edin.",
            "invalid_choice": "Zəhmət olmasa, seçim edin.",
            "required": "Zəhmət olmasa, seçim edin."
        }
    )

    mobile_number = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Zəhmət olmasa, məlumatları daxil edin.",
            "required": "Zəhmət olmasa, məlumatları daxil edin."
        }
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            "blank": "Zəhmət olmasa, məlumatları daxil edin.",
            "required": "Zəhmət olmasa, məlumatları daxil edin."
        }
    )

    password2 = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            "blank": "Zəhmət olmasa, məlumatları daxil edin.",
            "required": "Zəhmət olmasa, məlumatları daxil edin."
        }
    )

    profession_area = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),  # Modeli əlavə et
        error_messages={
            "required": "Zəhmət olmasa, peşə sahəsini daxil edin.",
            "null": "Zəhmət olmasa, peşə sahəsini daxil edin."
        }
    )

    profession_speciality = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),  # Modeli əlavə et
        error_messages={
            "required": "Zəhmət olmasa, peşə ixtisasını daxil edin.",
            "null": "Zəhmət olmasa, peşə ixtisasını daxil edin."
        }
    )

    experience_years = serializers.IntegerField(
        required=False,
        allow_null=True,
        error_messages={
            "invalid": "Zəhmət olmasa, iş təcrübəsini daxil edin.",
            "required": "Zəhmət olmasa, iş təcrübəsini daxil edin."
        }
    )

    education = serializers.ChoiceField(
        choices=[('0', 'Yoxdur'), ('1', 'Tam ali'), ('2', 'Natamam ali'), ('3', 'Orta'), ('4', 'Peşə təhsili'), ('5', 'Orta ixtisas təhsili')],
        error_messages={
            "invalid_choice": "Zəhmət olmasa, təhsil səviyyəsini daxil edin.",
            "required": "Zəhmət olmasa, təhsil səviyyəsini daxil edin."
        }
    )

    education_speciality = serializers.CharField(
        required=False,
        allow_blank=True,
        error_messages={
            "invalid": "Zəhmət olmasa, təhsil ixtisasını daxil edin.",
            "required": "Zəhmət olmasa, təhsil ixtisasını daxil edin."
        }
    )

    cities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=City.objects.all(),  # City modeli əlavə et
        required=False,
        allow_null=True,
        error_messages={
            "required": "Şəhər seçimi mütləqdir.",
            "incorrect_type": "Fəaliyyət ərazisi seçilməlidir."
        }
    )

    districts = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=District.objects.all(),  # District modeli əlavə et
        required=False,
        allow_null=True,
        error_messages={
            "required": "Rayon seçimi mütləqdir.",
            "incorrect_type": "Fəaliyyət ərazisi seçilməlidir."
        }
    )

    languages = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Language.objects.all(),  # Language modeli əlavə et
        error_messages={
            "required": "Zəhmət olmasa, dil biliklərinizi seçinnn.",
            "incorrect_type": "Zəhmət olmasa, dil biliklərinizi seçin."
        }
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=1500,
        error_messages={
            "max_length": "Əlavə qeyd 1500 simvoldan çox ola bilməz."
        }
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

        cities = request_data.get('cities')

        if cities is None:
            self.fields['districts'].required = True

##########//  Şəxsi məlumatlar  \\##########
    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Zəhmət olmasa, məlumatları daxil edin.")
        if value and not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError("Yalnız Azərbaycan hərfləri ilə qeyd edilməlidir.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Ad ən azı 3 simvol olmalıdır.")
        if len(value.strip()) > 21:
            raise serializers.ValidationError("Ad ən çoxu 20 simvol olmalıdır.")
        return value    


    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Zəhmət olmasa, məlumatları daxil edin.")
        if value and not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError("Yalnız Azərbaycan hərfləri ilə qeyd edilməlidir.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Soyad ən azı 3 simvol olmalıdır.")
        if len(value.strip()) > 21:
            raise serializers.ValidationError("Soyad ən çoxu 20 simvol olmalıdır.")
        return value
    
    def validate_birth_date(self, value):
        from datetime import date, datetime
        if not value:
            raise serializers.ValidationError("Zəhmət olmasa, məlumatları daxil edin.")

        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y/%m/%d").date()
            except ValueError:
                raise serializers.ValidationError("Doğum tarixi 'YYYY/MM/DD' formatında olmalıdır. Məsələn: 2000/01/30")
            
        # Yaş hesablaması
        today = date.today()
        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )

        if age < 16:
            raise serializers.ValidationError("Qeydiyyatdan keçmək üçün minimum yaş 16 olmalıdır.")

        return value

    def validate_mobile_number(self, value):
        if not value:
            raise serializers.ValidationError("Zəhmət olmasa, məlumatları daxil edin.")

        def check_number(phone):
            flag1 = False
            flag2 = False
            flag3 = False
            print(phone)

            valid_prefixes = ['10', '50', '51', '55', '70', '77', '99']
            prefix = phone[:2]

            if prefix in valid_prefixes:
                flag1 = True

            if phone.isdigit():
                flag2 = True

            if len(phone) == 9:
                flag3 = True

            if flag1 and flag2 and flag3:
                return False
            else:
                return True
            
        if check_number(phone=value):
            raise serializers.ValidationError("Mobil nömrə düzgün daxil edilməyib. 501234567 formatında daxil edin.")

        if CustomUser.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Bu mobil nömrə ilə istifadəçi artıq mövcuddur. Zəhmət olmasa, başqa mobil nömrə daxil edin.")

        return value

    def validate_gender(self, value):
        if not value:
            raise serializers.ValidationError("Zəhmət olmasa, seçim edin.")
        return value

    def validate_password(self, value):
        if len(value) < 8 or len(value) > 16:
            raise serializers.ValidationError("Şifrəniz 8 - 15 simvol aralığından ibarət olmalı, özündə minimum bir böyük hərf, rəqəm və xüsusi simvol (məsələn: !, @, #, -, _, +) ehtiva etməlidir.")

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Şifrəniz 8 - 15 simvol aralığından ibarət olmalı, özündə minimum bir böyük hərf, rəqəm və xüsusi simvol (məsələn: !, @, #, -, _, +) ehtiva etməlidir.")

        if not re.search(r'\d', value):
            raise serializers.ValidationError("Şifrəniz 8 - 15 simvol aralığından ibarət olmalı, özündə minimum bir böyük hərf, rəqəm və xüsusi simvol (məsələn: !, @, #, -, _, +) ehtiva etməlidir.")

        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', value):
            raise serializers.ValidationError("Şifrəniz 8 - 15 simvol aralığından ibarət olmalı, özündə minimum bir böyük hərf, rəqəm və xüsusi simvol (məsələn: !, @, #, -, _, +) ehtiva etməlidir.")

        return value


##########//  Peşə məlumatları  \\##########
    def validate_profession_area(self, value):
        if not value:
            raise serializers.ValidationError("Zəhmət olmasa, peşə sahəsini daxil edin.")
        return value
    
    def validate_profession_speciality(self, value):
        if not value:
            raise serializers.ValidationError("Zəhmət olmasa, peşə ixtisasını daxil edin.")
        return value
    
    def validate_custom_profession(self, value):
        if value and any(char.isdigit() for char in value):
            raise serializers.ValidationError("Yalnız Azərbaycan hərfləri ilə qeyd edilməlidir.")
        if value and len(value.strip()) > 51:
            raise serializers.ValidationError("Xüsusi ixtisas sahəsi ən çoxu 50 simvol olmalıdır.")
        return value
    
    def validate_experience_years(self, value):
        if not value:
            raise serializers.ValidationError("Zəhmət olmasa, iş təcrübəsini daxil edin.")
        if value < 0:
            raise serializers.ValidationError("İş təcrübəsi mənfi ədəd ola bilməz.")
        if value > 100:
            raise serializers.ValidationError("İş təcrübəsi 100 ildən çox ola bilməz.")
        return value
    

##########//  Təhsil məlumatları  \\##########
    def validate_education(self, value):
        if not value.strip():
            raise serializers.ValidationError("Zəhmət olmasa, təhsil səviyyəsini daxil edin.")
        return value

    def validate_education_speciality(self, value):
        if value and any(char.isdigit() for char in value):
            raise serializers.ValidationError("Yalnız Azərbaycan hərfləri ilə qeyd edilməlidir.")
        if len(value.strip()) > 51:
            raise serializers.ValidationError("Təhsil ixtisası ən çoxu 50 simvol olmalıdır.")
        return value
    
    def validate_languages(self, value):
        if not value:
            raise serializers.ValidationError("Zəhmət olmasa, dil biliklərinizi seçin.")
        return value

    def validate_note(self, value):
        if value and any(char.isdigit() for char in value):
            raise serializers.ValidationError("Yalnız Azərbaycan hərfləri ilə qeyd edilməlidir.")
        if value and len(value.strip()) > 1501:
            raise serializers.ValidationError("Əlavə qeyd ən çoxu 1500 simvol olmalıdır.")
        return value

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if not password:
            raise serializers.ValidationError({"password": "Zəhmət olmasa, məlumatları daxil edin."})
        
        if not password2:
            raise serializers.ValidationError({"password2": "Zəhmət olmasa, məlumatları daxil edin."})

        if password != password2:
            raise serializers.ValidationError({"password": "Şifrələr uyğun deyil."})

        profession_speciality = attrs.get('profession_speciality')
        custom_profession = attrs.get('custom_profession')

        speciality_name = getattr(profession_speciality, 'name', profession_speciality)
        if speciality_name == 'other':
            if not custom_profession:
                raise serializers.ValidationError({
                    'custom_profession': f"Zəhmət olmasa, peşə ixtisasını daxil edin."
                })
        else:
            if not profession_speciality:
                raise serializers.ValidationError({
                    'profession_speciality': 'Zəhmət olmasa, peşə ixtisasını daxil edin.'
                })
        
        # Təhsil üçün yoxlanış
        education = attrs.get("education")
        speciality = attrs.get("education_speciality")

        if education != "0" and not speciality:
            raise serializers.ValidationError({
                "education_speciality": "Zəhmət olmasa, təhsil ixtisasını daxil edin."
            })
        
        cities = attrs.get('cities')
        districts = attrs.get('districts')

        if not cities and not districts:
            raise serializers.ValidationError({
                "cities": "Fəaliyyət ərazisi seçilməlidir."
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
        
        if education_speciality != 'other':
            custom_profession = validated_data.pop('custom_profession', '')

        cities = validated_data.pop('cities', [])
        districts = validated_data.pop('districts', [])
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

        if cities is None and districts is not None:
            user.districts.set(extract_ids(districts))
        elif cities is not None and districts is None:
            user.cities.set(extract_ids(cities))
        elif cities is not None and districts is not None:
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