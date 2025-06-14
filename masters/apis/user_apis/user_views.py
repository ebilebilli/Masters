from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers.user_serializers import(
    RegisterSerializer,
    LoginSerializer,
)
from rest_framework.generics import CreateAPIView

from users.serializers.work_image_serializers import WorkImageSerializer
from users.models import WorkImage


class WorkImageCreateAPIView(CreateAPIView):
    queryset = WorkImage.objects.all()
    serializer_class = WorkImageSerializer


work_images_field = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(type=openapi.TYPE_FILE, format='binary'),
    description="İş şəkilləri (bir neçə fayl)",
    nullable=True,
)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Form-data ilə istifadəçi qeydiyyatı",
        operation_description="Fayl yükləmələri ilə istifadəçi qeydiyyatı",
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Ad", required=True),
            openapi.Parameter('last_name', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Soyad", required=True),
            openapi.Parameter('birth_date', openapi.IN_FORM, type=openapi.TYPE_STRING, format='date', description="Doğum tarixi", required=True),
            openapi.Parameter('gender', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Cins", required=True),
            openapi.Parameter('mobile_number', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Mobil nömrə", required=True),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING, format='password', description="Şifrə", required=True),
            openapi.Parameter('password2', openapi.IN_FORM, type=openapi.TYPE_STRING, format='password', description="Şifrə təsdiqi", required=True),
            openapi.Parameter('cities', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="Şəhərlərin ID-ləri", collectionFormat='multi', required=True),
            openapi.Parameter('districts', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="Rayonların ID-ləri", collectionFormat='multi', required=False),
            openapi.Parameter('languages', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="Dillərin ID-ləri", collectionFormat='multi', required=True),
            openapi.Parameter('profession_area', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description="Peşə sahəsi ID", required=True),
            openapi.Parameter('profession_speciality', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Peşə ixtisası", required=False),
            openapi.Parameter('custom_profession', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Xüsusi peşə", required=False),
            openapi.Parameter('experience_years', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description="İş təcrübəsi ili", required=True),
            openapi.Parameter('education', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Təhsil səviyyəsi", required=True),
            openapi.Parameter('education_speciality', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Təhsil ixtisası", required=False),
            openapi.Parameter('profile_image', openapi.IN_FORM, type=openapi.TYPE_FILE, description="Profil şəkli", required=False),
            openapi.Parameter('work_images', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_FILE), description="İş şəkilləri", collectionFormat='multi', required=False),
            openapi.Parameter('facebook', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Facebook URL", required=False),
            openapi.Parameter('instagram', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Instagram URL", required=False),
            openapi.Parameter('tiktok', openapi.IN_FORM, type=openapi.TYPE_STRING, description="TikTok URL", required=False),
            openapi.Parameter('linkedin', openapi.IN_FORM, type=openapi.TYPE_STRING, description="LinkedIn URL", required=False),
            openapi.Parameter('note', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Qeyd", required=False),
        ],
        responses={
            201: openapi.Response(description='Uğurlu qeydiyyat'),
            400: openapi.Response(description='Validasiya xətası')
        },
        examples={
            'multipart/form-data': {
                'first_name': 'Ali',
                'last_name': 'Vəliyev',
                'birth_date': '1990-01-01',
                'gender': 'male',
                'mobile_number': '+994501234567',
                'password': 'securepassword123',
                'password2': 'securepassword123',
                'cities': [1, 2],
                'districts': [3],
                'languages': [1],
                'profession_area': 1,
                'profession_speciality': 'Proqramçı',
                'custom_profession': 'Veb tərtibatçı',
                'experience_years': 5,
                'education': 'Bakalavr',
                'education_speciality': 'Kompüter elmləri',
                'facebook': 'https://facebook.com/ali.valiyev',
                'instagram': 'https://instagram.com/ali_valiyev',
                'tiktok': '',
                'linkedin': '',
                'profile_image': 'Profil şəkli faylı (məsələn, image.jpg)',
                'work_images': ['İş şəkli 1 (məsələn, work1.jpg)', 'İş şəkli 2 (məsələn, work2.jpg)'],
                'note': 'Əlavə qeyd'
            }
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Qeydiyyat uğurla tamamlandı."}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class TestAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user

#         if user:
#             return Response({'mobile_number': user.mobile_number,
#                             'first_name': user.first_name})
#         else:
#             return Response({'detal': 'ok'})
        


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="İstifadəçinin çıxışı (logout)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token")
            }
        ),
        responses={
            205: openapi.Response(description="Çıxış uğurla tamamlandı."),
            400: openapi.Response(description="Token düzgün deyil və ya artıq blacklistdədir.")
        }
    )

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Çıxış uğurla tamamlandı."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"detail": "Token düzgün deyil və ya artıq blacklistdədir."}, status=status.HTTP_400_BAD_REQUEST)




class UserDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="İstifadəçi profilinin deaktiv edilməsi (silinməsi əvəzinə)",
        responses={
            204: openapi.Response(description="Profil deaktiv edildi (is_active=False)"),
            401: openapi.Response(description="Avtorizasiya tələb olunur")
        }
    )
    @transaction.atomic
    def delete(self, request):
        user = request.user

        # Tokenləri blackliste at
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        # İstifadəçini tam silmək əvəzinə deaktiv et
        user.is_active = False
        user.save()

        return Response({"detail": "İstifadəçi uğurla silindi."}, status=status.HTTP_204_NO_CONTENT)