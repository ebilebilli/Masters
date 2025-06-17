from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers.profile_serializers import ProfileSerializer, ProfileUpdateSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

__all__ = [
    'ProfileAPIView',
    'ProfileUpdateAPIView',
    'ProfileDeleteAPIView'
]


class ProfileAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_summary="İstifadəçi profil məlumatlarının gətirilməsi",
        responses={
            200: openapi.Response(
                description="İstifadəçi profil məlumatları",
                schema=ProfileSerializer()
            ),
            403: "Bu səhifə əlçatan deyil",
            401: "Avtorizasiya tələb olunur"
        },
        security=[{"Bearer": []}]
    )

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProfileUpdateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 
    http_method_names = ['patch']

    @swagger_auto_schema(
        operation_summary="Profil yeniləməsi",
        operation_description="İstifadəçi profilini yeniləmək",
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Ad", required=False),
            openapi.Parameter('last_name', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Soyad", required=False),
            openapi.Parameter('birth_date', openapi.IN_FORM, type=openapi.TYPE_STRING, format='date', description="Doğum tarixi", required=False),
            openapi.Parameter('gender', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Cins", required=False),
            openapi.Parameter('mobile_number', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Mobil nömrə", required=False),
            openapi.Parameter('profession_area', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description="Peşə sahəsi ID", required=False),
            openapi.Parameter('profession_speciality', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description="Peşə ixtisası ID", required=False),
            openapi.Parameter('custom_profession', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Xüsusi peşə", required=False),
            openapi.Parameter('experience_years', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description="İş təcrübəsi ili", required=False),
            openapi.Parameter('education', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Təhsil səviyyəsi", required=False),
            openapi.Parameter('education_speciality', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Təhsil ixtisası", required=False),
            openapi.Parameter('cities', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="Şəhərlərin ID-ləri", collectionFormat='multi', required=False),
            openapi.Parameter('languages', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="Dillərin ID-ləri", collectionFormat='multi', required=False),
            openapi.Parameter('work_images', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="İş şəkillərinin ID-ləri (max 10)", collectionFormat='multi', required=False),
            openapi.Parameter('profile_image', openapi.IN_FORM, type=openapi.TYPE_FILE, description="Profil şəkli", required=False),
            openapi.Parameter('facebook', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Facebook URL", required=False),
            openapi.Parameter('instagram', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Instagram URL", required=False),
            openapi.Parameter('tiktok', openapi.IN_FORM, type=openapi.TYPE_STRING, description="TikTok URL", required=False),
            openapi.Parameter('linkedin', openapi.IN_FORM, type=openapi.TYPE_STRING, description="LinkedIn URL", required=False),
            openapi.Parameter('note', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Qeyd", required=False),
        ],
        responses={
        200: openapi.Response(
            description="Yenilənmiş profil məlumatları",
            schema=ProfileUpdateSerializer()
        ),
        400: "Validation error",
        401: "Unauthorized",
        403: "Forbidden"
    },
        security=[{"Bearer": []}]
    )
    def patch(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="İstifadəçi profilinin deaktiv edilməsi",
        responses={
            200: openapi.Response(description="Profil deaktiv edildi"),
            401: "Authorization tələb olunur",
        },
        security=[{"Bearer": []}]
    )

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()

        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response({'message': 'Profiliniz uğurla deaktiv edildi'}, status=status.HTTP_204_NO_CONTENT)
        

  