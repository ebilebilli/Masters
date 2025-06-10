import hashlib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models.user_model import CustomUser
from utils.paginations import CustomPagination


class SearchAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    search_param = openapi.Parameter('search', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING)
    profession_area_id_param = openapi.Parameter('profession_area_id', openapi.IN_QUERY, description="Profession area", type=openapi.TYPE_INTEGER)
    profession_speciality_id_param = openapi.Parameter('profession_speciality_id', openapi.IN_QUERY, description="Profession speciality", type=openapi.TYPE_INTEGER)
    city_id_param = openapi.Parameter('city_id', openapi.IN_QUERY, description="City ID", type=openapi.TYPE_INTEGER)
    district_id_param = openapi.Parameter('district_id', openapi.IN_QUERY, description="District ID", type=openapi.TYPE_INTEGER)
    language_id_param = openapi.Parameter('language_id', openapi.IN_QUERY, description="Language ID", type=openapi.TYPE_INTEGER)
    education_param = openapi.Parameter('education', openapi.IN_QUERY, description="Education level", type=openapi.TYPE_STRING)
    experience_years_param = openapi.Parameter('experience_years', openapi.IN_QUERY, description="Experience years", type=openapi.TYPE_INTEGER)
    ordering_param = openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by field", type=openapi.TYPE_STRING)
    page_param = openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER)
    page_size_param = openapi.Parameter('page_size', openapi.IN_QUERY, description="Page size", type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(
        manual_parameters=[
            search_param,
            profession_area_id_param,
            profession_speciality_id_param,
            city_id_param,
            district_id_param,
            language_id_param,
            education_param,
            experience_years_param,
            ordering_param,
            page_param,
            page_size_param
        ],
        operation_summary="Search and filter masters",
        operation_description="Search with filters and keywords"
    )
    def get(self, request):
        query_params = request.GET.urlencode()
        cache_key = f'search_{hashlib.md5(query_params.encode()).hexdigest()}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        search_query = request.query_params.get('search', '')
        profession_area_id = request.query_params.get('profession_area_id')
        profession_speciality_id = request.query_params.get('profession_speciality_id')
        city_id = request.query_params.get('city_id')
        district_id = request.query_params.get('district_id')
        language_id = request.query_params.get('language_id')
        education = request.query_params.get('education')
        experience_years = request.query_params.get('experience_years')
        ordering = request.query_params.get('ordering', '-id')

        queryset = CustomUser.objects.all()

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(custom_profession__icontains=search_query) |
                Q(education_speciality__icontains=search_query)
            )

        if profession_area_id:
            queryset = queryset.filter(profession_area_id=profession_area_id)

        if profession_speciality_id:
            queryset = queryset.filter(profession_speciality_id=profession_speciality_id)

        if city_id:
            queryset = queryset.filter(cities__id=city_id)

        if district_id:
            queryset = queryset.filter(districts__id=district_id)

        if language_id:
            queryset = queryset.filter(languages__id=language_id)

        if education:
            queryset = queryset.filter(education=education)

        if experience_years:
            try:
                queryset = queryset.filter(experience_years=int(experience_years))
            except ValueError:
                pass

        queryset = queryset.order_by(ordering)
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Sonuçları hazırla
        response_data = [
            {
                'id': master.id,
                'first_name': master.first_name,
                'last_name': master.last_name,
                'profession_area': master.profession_area.name if master.profession_area else '',
                'profession_speciality': master.profession_speciality.name if master.profession_speciality else '',
                'city': [city.name for city in master.cities.all()],
                'district': [district.name for district in master.districts.all()],
                'language': [language.name for language in master.languages.all()],
                'education': master.education,
                'experience_years': master.experience_years
            } for master in paginated_queryset
        ]

        paginated_response = paginator.get_paginated_response(response_data)
        cache.set(cache_key,paginated_response.data, timeout=250)

        return Response(paginated_response, status=status.HTTP_200_OK)