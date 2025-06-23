import hashlib
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Avg
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models.user_model import CustomUser
from users.serializers.user_serializers import CustomUserSerializer
from utils.paginations import CustomPagination




class SearchAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    search_param = openapi.Parameter('search', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING)
    profession_area_id_param = openapi.Parameter('profession_area_id', openapi.IN_QUERY, description="Profession area", type=openapi.TYPE_INTEGER)
    profession_speciality_id_param = openapi.Parameter('profession_speciality_id', openapi.IN_QUERY, description="Profession speciality", type=openapi.TYPE_INTEGER)
    city_id_param = openapi.Parameter('city_id', openapi.IN_QUERY, description="City ID", type=openapi.TYPE_INTEGER)
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
    def get(self, request, *args, **kwargs):
        query_params = request.GET.urlencode()
        cache_key = f'search_{hashlib.md5(query_params.encode()).hexdigest()}'
        cached_data = cache.get(cache_key)

        if cached_data:
            if isinstance(cached_data, dict):
                return Response(cached_data, status=status.HTTP_200_OK)
            else:
                cache.delete(cache_key)

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            cache.set(cache_key, paginated_response.data, timeout=250)
            return paginated_response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        request = self.request
        search_query = request.query_params.get('search', '')
        profession_area_id = request.query_params.get('profession_area_id')
        profession_speciality_id = request.query_params.get('profession_speciality_id')
        city_id = request.query_params.get('city_id')
        language_id = request.query_params.get('language_id')
        education = request.query_params.get('education')
        experience_years = request.query_params.get('experience_years')
        ordering = request.query_params.get('ordering', '-id')

        queryset = CustomUser.objects.filter(is_active=True, is_master=True)

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

        if language_id:
            queryset = queryset.filter(languages__id=language_id)

        if education:
            queryset = queryset.filter(education=education)

        if experience_years:
            try:
                queryset = queryset.filter(experience_years=int(experience_years))
            except ValueError:
                pass
        
        if ordering.lstrip('-') == 'rating':
            queryset = queryset.annotate(rating=Avg('reviews__rating'))

        return queryset.order_by(ordering)
