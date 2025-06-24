from PIL import Image
from rest_framework import serializers

from services.models.category_model import Category
from services.models.service_model import Service
from core.models.city_model import City, District
from core.models.language_model import Language
from users.models import CustomUser
from users.models import  WorkImage


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile_image = serializers.ImageField()
    profession_speciality = serializers.StringRelatedField()
    profession_area = serializers.StringRelatedField()
    languages = serializers.StringRelatedField(many=True)
    cities = serializers.SerializerMethodField()
    districts = serializers.SerializerMethodField()
    work_images = serializers.StringRelatedField(many=True)

    average_rating = serializers.SerializerMethodField()
    average_responsible = serializers.SerializerMethodField()
    average_neat = serializers.SerializerMethodField()
    average_time_management = serializers.SerializerMethodField()
    average_communicative = serializers.SerializerMethodField()
    average_punctual = serializers.SerializerMethodField()
    average_professional = serializers.SerializerMethodField()
    average_experienced = serializers.SerializerMethodField()
    average_efficient = serializers.SerializerMethodField()
    average_agile = serializers.SerializerMethodField()
    average_patient = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'full_name',
            'profile_image',
            'note',
            'gender',
            'birth_date',
            'mobile_number',
            'facebook',
            'instagram',
            'tiktok',
            'linkedin',
            'profession_speciality',
            'profession_area',
            'custom_profession',
            'education',
            'education_speciality',
            'experience_years',
            'languages',
            'cities',
            'districts',
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
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
        
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

    def get_cities(self, obj):
        return [city.display_name for city in obj.cities.all()]

    def get_districts(self, obj):
        return [district.display_name for district in obj.districts.all()]

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_average_responsible(self, obj):
        return obj.average_responsible

    def get_average_neat(self, obj):
        return obj.average_neat

    def get_average_time_management(self, obj):
        return obj.average_time_management

    def get_average_communicative(self, obj):
        return obj.average_communicative

    def get_average_punctual(self, obj):
        return obj.average_punctual

    def get_average_professional(self, obj):
        return obj.average_professional

    def get_average_experienced(self, obj):
        return obj.average_experienced

    def get_average_efficient(self, obj):
        return obj.average_efficient

    def get_average_agile(self, obj):
        return obj.average_agile

    def get_average_patient(self, obj):
        return obj.average_patient

    def get_review_count(self, obj):
        return obj.review_count
     

class ProfileUpdateSerializer(serializers.ModelSerializer):
    profession_area = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    profession_speciality = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), required=False)
    cities = serializers.PrimaryKeyRelatedField(many=True, queryset=City.objects.all(), required=False)
    districts = serializers.PrimaryKeyRelatedField(many=True, queryset=District.objects.all(), required=False)
    languages = serializers.PrimaryKeyRelatedField(many=True, queryset=Language.objects.all(), required=False)
    profile_image = serializers.ImageField(required=False)
    work_images = serializers.PrimaryKeyRelatedField(many=True, queryset=WorkImage.objects.all(), required=False)


    class Meta:
        model = CustomUser
        fields = [
            "first_name", "last_name", "birth_date", "gender", "mobile_number",
            "profession_area", "profession_speciality", "custom_profession", "experience_years",'work_images',
            "cities",  "districts", "education", "education_speciality", "languages",
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

        cities = attrs.get("cities") or user.cities.all()
        districts = attrs.get("districts") or user.districts.all()

        if not cities and not districts:
            raise serializers.ValidationError('Şəhər və rayonlardan ən azı biri seçilməldir')

        # if districts and not any(city.name == 'baku' for city in cities):
        #     raise serializers.ValidationError('Rayonlar sadəcə Bakı şəhəri üçün mövcuddur.')
        
        # if not districts and any(city.name == 'baku' for city in cities):
        #     raise serializers.ValidationError('Bakı şəhəri seçilibsə Bakı üçün rayonlar seçilməlidir.')

        return attrs
    
    def validate_work_images(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("Ən çox 10 iş şəkli seçilə bilər.")

        for image_obj in value:
            try:
                img_field = image_obj.image
            except AttributeError:
                raise serializers.ValidationError("Şəkil obyektində 'image' sahəsi yoxdur.")

            if img_field.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(f"{img_field.name} faylı 5MB-dan böyükdür.")

            try:
                img = Image.open(img_field)
                img.verify()
                if img.format not in ['JPEG', 'JPG', 'PNG']:
                    raise serializers.ValidationError(
                        f"{img_field.name} şəkil formatı uyğun deyil. Yalnız JPG və PNG formatları dəstəklənir."
                    )
            except Exception:
                raise serializers.ValidationError(f"{img_field.name} faylı şəkil deyil və ya zədəlidir.")

        return value

    def update(self, instance, validated_data):
        cities = validated_data.pop("cities", None)
        districts = validated_data.pop("districts", None)
        languages = validated_data.pop("languages", None)
        work_images = validated_data.pop("work_images", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if cities is not None:
            instance.cities.set(cities)
        
        if districts is not None:
            instance.districts.set(districts)

        if languages is not None:
            instance.languages.set(languages)

        if work_images is not None:
            instance.work_images.set(work_images)

        instance.save()
        return instance