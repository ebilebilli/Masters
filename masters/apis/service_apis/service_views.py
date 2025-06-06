from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from services.models.category_model import Category
from services.models.service_model import Service
from services.serializers.service_serializer import ServiceSerializer
from users.models.user_model import CustomUser
#from users.serializers.user_serializers import CustomUserSerializer
from utils.paginations import CustomPagination


__all__ = [
    'ServicesForCategoryAPIView',
    'MasterListForServicesAPIView'
]

class ServicesForCategoryAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request, category_id):
        try:
            category = get_object_or_404(Category, id=category_id)
            services = Service.objects.filter(category=category)
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'error': 'Axtarılan kategoriya yoxdur'})


# class MasterListForServicesAPIView(APIView):
#     permission_classes = [AllowAny]
#     pagination_class =  CustomPagination
#     http_method_names = ['get']

#     def get(self, request, service_id):
#         pagination = self.pagination_class()
#         service = get_object_or_404(Service, id=service_id)
#         masters =  CustomUser.objects.filter(profession_service=service, is_active=True)
#         if not masters.exists():
#             return Response({
#                 'error': 'Hal-hazırda bu servisə uyğun aktif bir usta yoxdur'
#             },status=status.HTTP_404_NOT_FOUND)
#         result_page = pagination.paginate_queryset(masters, request)
#         serializer = MasterSerializer(result_page, many=True)
#         paginated_response = pagination.get_paginated_response(serializer.data).data
#         return Response(paginated_response, status=status.HTTP_200_OK)
