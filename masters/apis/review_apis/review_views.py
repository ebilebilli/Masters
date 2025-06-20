from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
        reviews = Review.objects.filter(master=master)
        result_page = pagination.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        return Response(paginated_response, status=status.HTTP_200_OK)

class CreateReviewAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description="Yeni rəy əlavə edir.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING, description="Rəy mətni"),
                'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description="Reytinq (1-5)"),
                'review_images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_FILE),
                    description="Şəkillər (max 3)",
                    maxItems=3
                ),
            },
            required=['text', 'rating']
        ),
        responses={
            201: ReviewSerializer(),
            403: openapi.Response('Özünüzə şərh əlavə edə bilmərsiniz'),
            404: openapi.Response('Usta tapılmadı')
        }
    )
    @transaction.atomic
    def post(self, request, master_id):
        user = request.user
        if user.id == master_id:
            return Response({'error': 'Özünüzə şərh əlavə edə bilmərsiniz'}, status=status.HTTP_403_FORBIDDEN)
        master = get_object_or_404(CustomUser, is_active=True, id=master_id)
        serializer = ReviewSerializer(data=request.data, context={'user': user, 'master': master})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateReviewAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['patch']

    @swagger_auto_schema(
        operation_description="Mövcud rəyin məlumatlarını yeniləyir.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING, description="Rəy mətni"),
                'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description="Reytinq (1-5)"),
                'review_images': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_FILE),
                    description="Şəkillər (max 3)",
                    maxItems=3
                ),
            }
        ),
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        master = get_object_or_404(CustomUser, is_active=True, id=master_id)
        order = request.query_params.get('order', 'newest')
        reviews = Review.objects.filter(master=master).order_by('created_at' if order == 'oldest' else '-created_at')
        result_page = pagination.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(result_page, many=True)
        paginated_response = pagination.get_paginated_response(serializer.data).data
        return Response(paginated_response, status=status.HTTP_200_OK)