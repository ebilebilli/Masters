from elasticsearch import Elasticsearch
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.permissions import AllowAny
from utils.paginations import CustomPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


__all__ = [
    'SearchAPIView'
]

es_client = Elasticsearch(hosts=[settings.ELASTICSEARCH_HOST])

search_param = openapi.Parameter('search', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING)
profession_area_id_param = openapi.Parameter('profession_area_id', openapi.IN_QUERY, description="Filter by profession area ID", type=openapi.TYPE_INTEGER)
profession_speciality_id_param = openapi.Parameter('profession_speciality_id', openapi.IN_QUERY, description="Filter by profession speciality ID", type=openapi.TYPE_INTEGER)
city_id_param = openapi.Parameter('city_id', openapi.IN_QUERY, description="Filter by city ID", type=openapi.TYPE_INTEGER)
district_id_param = openapi.Parameter('district_id', openapi.IN_QUERY, description="Filter by district ID", type=openapi.TYPE_INTEGER)
language_id_param = openapi.Parameter('language_id', openapi.IN_QUERY, description="Filter by language ID", type=openapi.TYPE_INTEGER)
education_param = openapi.Parameter('education', openapi.IN_QUERY, description="Filter by education level", type=openapi.TYPE_STRING)
experience_years_param = openapi.Parameter('experience_years', openapi.IN_QUERY, description="Filter by exact years of experience", type=openapi.TYPE_INTEGER)
ordering_param = openapi.Parameter('ordering', openapi.IN_QUERY, description="Field to order by, e.g., 'experience_years', 'first_name.keyword'", type=openapi.TYPE_STRING)
page_param = openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER)
page_size_param = openapi.Parameter('page_size', openapi.IN_QUERY, description="Page size (max 100)", type=openapi.TYPE_INTEGER)

class SearchAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

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
        profession_area_id = request.GET.get('profession_area_id')
        profession_speciality_id = request.GET.get('profession_speciality_id')
        city_id = request.GET.get('city_id')
        district_id = request.GET.get('district_id')
        language_id = request.GET.get('language_id')
        education = request.GET.get('education')
        experience_years = request.GET.get('experience_years')
        search_query = request.GET.get('search')
        ordering = request.GET.get('ordering')

        must_filters = []

        if profession_area_id:
            must_filters.append({
                "term": {"profession_area.id": int(profession_area_id)}
            })

        if profession_speciality_id:
            must_filters.append({
                "term": {"profession_speciality.id": int(profession_speciality_id)}
            })

        if city_id:
            must_filters.append({
                "nested": {
                    "path": "cities",
                    "query": {
                        "term": {"cities.id": int(city_id)}
                    }
                }
            })

        if district_id:
            must_filters.append({
                "nested": {
                    "path": "districts",
                    "query": {
                        "term": {"districts.id": int(district_id)}
                    }
                }
            })

        if language_id:
            must_filters.append({
                "nested": {
                    "path": "languages",
                    "query": {
                        "term": {"languages.id": int(language_id)}
                    }
                }
            })

        if education:
            must_filters.append({
                "term": {"education": education}
            })

        if experience_years:
            try:
                must_filters.append({
                    "term": {"experience_years": int(experience_years)}
                })
            except ValueError:
                pass

        # Əsas query qurulması
        bool_query = {
            "must": must_filters
        }

        if search_query:
            # search_query varsa, onu must-ə əlavə et
            bool_query["must"].append({
                "multi_match": {
                    "query": search_query,
                    "fields": [
                        "first_name",
                        "last_name",
                        "custom_profession",
                        "education_speciality",
                        "profession_area.name",
                        "profession_speciality.name"
                    ]
                }
            })

            # cities, districts və languages üçün nested match-lər əlavə et
            bool_query["must"].extend([
                {
                    "nested": {
                        "path": "cities",
                        "query": {
                            "match": {"cities.name": search_query}
                        }
                    }
                },
                {
                    "nested": {
                        "path": "districts",
                        "query": {
                            "match": {"districts.name": search_query}
                        }
                    }
                },
                {
                    "nested": {
                        "path": "languages",
                        "query": {
                            "match": {"languages.name": search_query}
                        }
                    }
                }
            ])

        query_body = {
            "query": {
                "bool": bool_query
            }
        }

        if ordering:
            query_body["sort"] = [ordering]

        try:
            page = int(request.GET.get('page', 1))
            page_size = min(
                int(request.GET.get('page_size', CustomPagination.page_size)),
                CustomPagination.max_page_size
            )
        except ValueError:
            page = 1
            page_size = CustomPagination.page_size

        from_ = (page - 1) * page_size

        response = es_client.search(
            index="masters",
            body=query_body,
            size=page_size,
            from_=from_
        )

        results = [hit["_source"] for hit in response["hits"]["hits"]]
        pagination = CustomPagination()
        result_page = pagination.paginate_queryset(results, request, view=self)
        return pagination.get_paginated_response(result_page)