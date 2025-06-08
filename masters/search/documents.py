from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch import Elasticsearch
from django.conf import settings
import logging

from users.models.user_model import CustomUser
from users.models.work_image_model import WorkImage
from services.models.category_model import Category
from services.models.service_model import Service
from core.models.language_model import Language
from core.models.city_model import City, District

logger = logging.getLogger(__name__)

try:
    es_client = Elasticsearch(hosts=[settings.ELASTICSEARCH_HOST])
    if not es_client.ping():
        logger.warning("Elasticsearch serverinə qoşulma uğursuz oldu!")
        es_client = None
except Exception as e:
    logger.error(f"Elasticsearch bağlantısı zamanı xəta baş verdi: {e}")
    es_client = None


@registry.register_document
class MasterDocument(Document):
    profession_area = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'display_name': fields.TextField(),
    })

    profession_speciality = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'display_name': fields.TextField(),
    })

    cities = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'display_name': fields.TextField(),
    })

    districts = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'display_name': fields.TextField(),
    })

    languages = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
        'display_name': fields.TextField(),
    })

    work_images = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'image': fields.TextField(),
    })

    average_rating = fields.FloatField()
    average_responsible = fields.FloatField()
    average_neat = fields.FloatField()
    average_time_management = fields.FloatField()
    average_communicative = fields.FloatField()
    average_punctual = fields.FloatField()
    average_professional = fields.FloatField()
    average_experienced = fields.FloatField()
    average_efficient = fields.FloatField()
    average_agile = fields.FloatField()
    average_patient = fields.FloatField()
    review_count = fields.IntegerField()

    class Index:
        name = 'masters'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'mobile_number',
            'gender',
            'custom_profession',
            'experience_years',
            'education',
            'education_speciality',
            'profile_image',
            'facebook',
            'instagram',
            'tiktok',
            'linkedin',
            'note',
            'is_active',
            'created_at',
            'updated_at',
        ]
        related_models = [Category, Service, City, District, Language, WorkImage]

    def get_instances_from_related(self, related_instance):
        try:
            if isinstance(related_instance, Category):
                return CustomUser.objects.filter(profession_area=related_instance)
            elif isinstance(related_instance, Service):
                return CustomUser.objects.filter(profession_speciality=related_instance)
            elif isinstance(related_instance, City):
                return CustomUser.objects.filter(cities=related_instance)
            elif isinstance(related_instance, District):
                return CustomUser.objects.filter(districts=related_instance)
            elif isinstance(related_instance, Language):
                return CustomUser.objects.filter(languages=related_instance)
            elif isinstance(related_instance, WorkImage):
                return CustomUser.objects.filter(work_images=related_instance)
            return []
        except Exception:
            return []

    def prepare_average_rating(self, instance):
        return instance.average_rating() or None

    def prepare_average_responsible(self, instance):
        return instance.average_responsible or None

    def prepare_average_neat(self, instance):
        return instance.average_neat or None

    def prepare_average_time_management(self, instance):
        return instance.average_time_management or None

    def prepare_average_communicative(self, instance):
        return instance.average_communicative or None

    def prepare_average_punctual(self, instance):
        return instance.average_punctual or None

    def prepare_average_professional(self, instance):
        return instance.average_professional or None

    def prepare_average_experienced(self, instance):
        return instance.average_experienced or None

    def prepare_average_efficient(self, instance):
        return instance.average_efficient or None

    def prepare_average_agile(self, instance):
        return instance.average_agile or None

    def prepare_average_patient(self, instance):
        return instance.average_patient or None

    def prepare_review_count(self, instance):
        return instance.review_count or None

    def prepare_profession_area(self, instance):
        if instance.profession_area:
            return {
                'id': instance.profession_area.id,
                'name': instance.profession_area.name,
                'display_name': instance.profession_area.display_name
            }
        return None

    def prepare_profession_speciality(self, instance):
        if instance.profession_speciality:
            return {
                'id': instance.profession_speciality.id,
                'name': instance.profession_speciality.name,
                'display_name': instance.profession_speciality.display_name
            }
        return None

    def prepare_custom_profession(self, instance):
        return instance.custom_profession or None

    def prepare_cities(self, instance):
        return [
            {
                'id': city.id,
                'name': city.name,
                'display_name': getattr(city, 'display_name', None)
            }
            for city in instance.cities.all()
        ]

    def prepare_districts(self, instance):
        return [
            {
                'id': district.id,
                'name': district.name,
                'display_name': getattr(district, 'display_name', None)
            }
            for district in instance.districts.all()
        ]

    def prepare_languages(self, instance):
        return [
            {
                'id': language.id,
                'name': language.name,
                'display_name': getattr(language, 'display_name', None)
            }
            for language in instance.languages.all()
        ]

    def prepare_work_images(self, instance):
        return [
            {
                'id': image.id,
                'image': image.image.url if image.image else None
            }
            for image in instance.work_images.all()
        ]