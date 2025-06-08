from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Avg, Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models.user_model import CustomUser
from users.serializers.user_serializers import CustomUserSerializer
from utils.paginations import CustomPagination, PaginationForMainPage


__all__ = [
    'MastersListAPIView',
    'TopRatedMastersListAPIView',
    'MasterDetailAPIView',
    'MasterProfileUpdateAPIView',
    'MasterProfileDeleteAPIView'
]


class MastersListAPIView(APIView):
    """
    get:
    List all active masters with their average rating and number of reviews.
    """
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    http_method_names = ['get']
    
    @swagger_auto_schema(
        operation_summary="Aktiv ustaların siyahısı",
        operation_description="Orta reytinq və rəy sayı ilə birlikdə aktiv ustaları göstərir.",
        responses={200: CustomUserSerializer(many=True)}
    )

    def get(self, request):
        pagination = self.pagination_class()
        masters = CustomUser.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            count_ratings=Count('reviews')
        ).filter(is_active=True)
        
        if not masters.exists():
            return Response({
                'error': 'Hal-hazırda aktiv bir usta yoxdur'
            }, status=status.HTTP_404_NOT_FOUND)
        result_page = pagination.paginate_queryset(masters, request)
        serializer = CustomUserSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        return Response(paginated_response, status=status.HTTP_200_OK)


class TopRatedMastersListAPIView(APIView):
    """
    get:
    Return a list of top-rated active masters sorted by rating, review count, and last login.
    """
    permission_classes = [AllowAny]
    pagination_class = PaginationForMainPage
    http_method_names = ['get']
    
    @swagger_auto_schema(
        operation_summary="Ən yüksək reytinqli ustalar",
        operation_description="Reytinqə, rəy sayına və son daxil olmağa görə sıralanmış aktiv ustalar.",
        responses={200: CustomUserSerializer(many=True)}
    )

    def get(self, request):
        pagination = self.pagination_class()
        masters = CustomUser.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            count_ratings=Count('reviews')
        ).filter(is_active_on_main_page=True).order_by('-avg_rating', '-count_ratings', '-last_login')
        
        if not masters.exists():
            return Response({
                'error': 'Hal-hazırda aktiv bir usta yoxdur'
            }, status=status.HTTP_404_NOT_FOUND)
        result_page = pagination.paginate_queryset(masters, request)
        serializer = CustomUserSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        return Response(paginated_response, status=status.HTTP_200_OK)


class MasterDetailAPIView(APIView):
    """
    get:
    Retrieve a master's details by ID.

    patch:
    Update the master. Only the master themselves or a superuser can perform this.

    delete:
    Delete the master. Only the master themselves or a superuser can perform this.
    """

    http_method_names = ['get']
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_summary="Usta məlumatlarını göstər",
        responses={200: CustomUserSerializer()}
    )

    def get(self, request, master_id):
        master = get_object_or_404(CustomUser, id=master_id, is_active=True)
        serializer = CustomUserSerializer(master)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MasterProfileUpdateAPIView(APIView):
    """
    get:
    Retrieve a master's details by ID.

    patch:
    Update the master. Only the master themselves or a superuser can perform this.

    """
     
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    @swagger_auto_schema(
        operation_summary="Ustanı yenilə",
        request_body=CustomUserSerializer(partial=True),
        responses={
            200: CustomUserSerializer(),
            400: 'Daxil edilən məlumatlar səhvdir',
            403: 'İcazəniz yoxdur'
        }
    )

    def patch(self, request, master_id):
        user = request.user
        master = get_object_or_404(CustomUser, id=master_id)
        serializer = CustomUserSerializer(master, data=request.data, partial=True)
        if master.id != user.id and not user.is_superuser:
            return Response({'error': 'Bunu etməyə icazəniz yoxdur'}, status=status.HTTP_403_FORBIDDEN)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Daxil edilən məlumatlar səhvdir'}, status=status.HTTP_400_BAD_REQUEST)


class MasterProfileDeleteAPIView(APIView):
    """
    delete:
    Delete the master. Only the master themselves or a superuser can perform this.

    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']

    @swagger_auto_schema(
        operation_summary="Ustanı sil",
        responses={
            204: openapi.Response(description="Hesab silindi"),
            403: 'İcazəniz yoxdur'
        }
    )
    
    def delete(self, request, master_id):
        user = request.user
        master = get_object_or_404(CustomUser, id=master_id)
        if master.id != user.id and not user.is_superuser:
            return Response({'error': 'Bunu etməyə icazəniz yoxdur'}, status=status.HTTP_403_FORBIDDEN)
        
        master.delete()
        return Response({'message': 'Hesab silindi'}, status=status.HTTP_204_NO_CONTENT)
