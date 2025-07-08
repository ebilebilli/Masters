from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError

from reviews.models.review_models import Review
from users.models.user_model import CustomUser
from reviews.serializers.review_serializers import ReviewSerializer
from utils.paginations import PaginationForMainPage
from utils.permissions import HeHasPermission


__all__ = [
    'ReviewsForMasterAPIView',
    'CreateReviewAPIView',
    'UpdateReviewAPIView',
    'DeleteReviewAPIView',
    'FilterReviewAPIView'
]

class ReviewsForMasterAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = PaginationForMainPage
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_description="Verilmiş master ID-yə aid bütün rəyləri gətirir (səhifələnmiş).",
        responses={200: ReviewSerializer(many=True)},
    )
    def get(self, request, master_id):
        master = get_object_or_404(CustomUser, is_active=True, id=master_id)
        pagination = self.pagination_class()
        reviews = Review.objects.filter(master=master).order_by('-created_at')
        result_page = pagination.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data

        return Response(paginated_response, status=status.HTTP_200_OK)


class CreateReviewAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['post', 'get']

    @swagger_auto_schema(
        operation_description="Yeni rəy əlavə edir.",
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_FORM, description="İstifadəçi adı", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'comment', openapi.IN_FORM, description="Rəy mətni", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'rating', openapi.IN_FORM, description="Reytinq (1-5)", type=openapi.TYPE_INTEGER
            ),
             openapi.Parameter(
                'responsible', openapi.IN_FORM, description="Məsuliyyətli", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'neat', openapi.IN_FORM, description="Səliqəli", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'time_management', openapi.IN_FORM, description="Vaxta nəzarət", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'communicative', openapi.IN_FORM, description="Ünsiyyətcil", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'punctual', openapi.IN_FORM, description="Dəqiq", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'professional', openapi.IN_FORM, description="Peşəkar", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'experienced', openapi.IN_FORM, description="Təcrübəli", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'efficient', openapi.IN_FORM, description="Səmərəli", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'agile', openapi.IN_FORM, description="Çevik", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'patient', openapi.IN_FORM, description="Səbirli", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'review_images', openapi.IN_FORM, description="Şəkillər (max 3)", type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_FILE), maxItems=3, required=False
            ),
        ],
        responses={
            201: ReviewSerializer(),
            403: openapi.Response('Özünüzə şərh əlavə edə bilmərsiniz'),
            404: openapi.Response('Usta tapılmadı'),
            400: openapi.Response('Səhv məlumat')
        }
    )
    @transaction.atomic
    def post(self, request, master_id):
        user = request.user
        master = get_object_or_404(CustomUser, is_active=True, id=master_id)
        if user.id == master_id:
            return Response({'error': 'Özünüzə şərh əlavə edə bilmərsiniz'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ReviewSerializer(data=request.data, context={'master': master})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'Göndərilən sorğu düzgün deyil'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateReviewAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['patch']

    @swagger_auto_schema(
        operation_description="Mövcud rəyin məlumatlarını yeniləyir.",
        manual_parameters=[
            openapi.Parameter(
                'username', openapi.IN_FORM, description="İstifadəçi adı", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'comment', openapi.IN_FORM, description="Rəy mətni", type=openapi.TYPE_STRING, required=False
            ),
            openapi.Parameter(
                'rating', openapi.IN_FORM, description="Reytinq (1-5)", type=openapi.TYPE_INTEGER, required=False
            ),
             openapi.Parameter(
                'responsible', openapi.IN_FORM, description="Məsuliyyətli", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'neat', openapi.IN_FORM, description="Səliqəli", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'time_management', openapi.IN_FORM, description="Vaxta nəzarət", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'communicative', openapi.IN_FORM, description="Ünsiyyətcil", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'punctual', openapi.IN_FORM, description="Dəqiq", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'professional', openapi.IN_FORM, description="Peşəkar", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'experienced', openapi.IN_FORM, description="Təcrübəli", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'efficient', openapi.IN_FORM, description="Səmərəli", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'agile', openapi.IN_FORM, description="Çevik", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'patient', openapi.IN_FORM, description="Səbirli", type=openapi.TYPE_BOOLEAN, required=False
            ),
            openapi.Parameter(
                'review_images', openapi.IN_FORM, description="Şəkillər (max 3)", type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_FILE), maxItems=3, required=False
            ),
        ],
        responses={
            200: ReviewSerializer(),
            400: openapi.Response('Səhv məlumat'),
            404: openapi.Response('Rəy tapılmadı')
        }
    )
    @transaction.atomic
    def patch(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'error': 'Göndərilən sorğu düzgün deyil'},  status=status.HTTP_400_BAD_REQUEST)


class DeleteReviewAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    http_method_names = ['delete']

    @swagger_auto_schema(
        operation_description="Rəyi silir.",
        responses={204: openapi.Response('Uğurla silindi')}
    )
    @transaction.atomic
    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return Response({'message': 'Şərhiniz uğurla silindi'}, status=status.HTTP_204_NO_CONTENT)


class FilterReviewAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = PaginationForMainPage
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_description="Masterə aid rəyləri `order` parametri ilə sıralayıb qaytarır.",
        manual_parameters=[
            openapi.Parameter(
                'order', openapi.IN_QUERY, description="'newest' və ya 'oldest'", type=openapi.TYPE_STRING
            )
        ],
        responses={200: ReviewSerializer(many=True)}
    )
    def get(self, request, master_id):
        pagination = self.pagination_class()
        master = get_object_or_404(CustomUser, is_active=True, is_master=True, id=master_id)
        order = request.query_params.get('order', 'newest')

        if order == 'oldest':
            reviews = Review.objects.filter(master=master).order_by('created_at')
        else:
            reviews = Review.objects.filter(master=master).order_by('-created_at')

        result_page = pagination.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        return Response(paginated_response, status=status.HTTP_200_OK)
