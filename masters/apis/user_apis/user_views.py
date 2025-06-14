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

register_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=[
        'first_name', 'last_name', 'birth_date', 'gender', 'mobile_number',
        'password', 'password2', 'cities', 'languages', 'profession_area',
        'experience_years', 'education'
    ],
    properties={
        "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="Ad"),
        "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Soyad"),
        "birth_date": openapi.Schema(type=openapi.TYPE_STRING, format='date', description="Doğum tarixi"),
        "gender": openapi.Schema(type=openapi.TYPE_STRING, description="Cins"),
        "mobile_number": openapi.Schema(type=openapi.TYPE_STRING, description="Mobil nömrə"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, format='password', description="Şifrə"),
        "password2": openapi.Schema(type=openapi.TYPE_STRING, format='password', description="Şifrə təsdiqi"),
        "cities": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER),
            description="Şəhərlərin ID-ləri"
        ),
        "districts": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER),
            description="Rayonların ID-ləri",
            nullable=True
        ),
        "languages": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_INTEGER),
            description="Dillərin ID-ləri"
        ),
        "profession_area": openapi.Schema(type=openapi.TYPE_INTEGER, description="Peşə sahəsi ID"),
        "profession_speciality": openapi.Schema(type=openapi.TYPE_STRING, description="Peşə ixtisası", nullable=True),
        "custom_profession": openapi.Schema(type=openapi.TYPE_STRING, description="Xüsusi peşə", nullable=True),
        "experience_years": openapi.Schema(type=openapi.TYPE_INTEGER, description="İş təcrübəsi ili"),
        "education": openapi.Schema(type=openapi.TYPE_STRING, description="Təhsil səviyyəsi"),
        "education_speciality": openapi.Schema(type=openapi.TYPE_STRING, description="Təhsil ixtisası", nullable=True),
        "profile_image": openapi.Schema(type=openapi.TYPE_FILE, format='binary', description="Profil şəkli", nullable=True),
        "facebook": openapi.Schema(type=openapi.TYPE_STRING, description="Facebook URL", nullable=True),
        "instagram": openapi.Schema(type=openapi.TYPE_STRING, description="Instagram URL", nullable=True),
        "tiktok": openapi.Schema(type=openapi.TYPE_STRING, description="TikTok URL", nullable=True),
        "linkedin": openapi.Schema(type=openapi.TYPE_STRING, description="LinkedIn URL", nullable=True),
        "work_images": work_images_field,
        "note": openapi.Schema(type=openapi.TYPE_STRING, description="Qeyd", nullable=True),
    }
)

# Form-data nümunəsi
register_form_data_example = {
    "first_name": "Ali",
    "last_name": "Vəliyev",
    "birth_date": "1990-01-01",
    "gender": "male",
    "mobile_number": "+994501234567",
    "password": "securepassword123",
    "password2": "securepassword123",
    "cities": [1, 2],
    "districts": [3],
    "languages": [1],
    "profession_area": 1,
    "profession_speciality": 1,
    "custom_profession": "Veb tərtibatçı",
    "experience_years": 5,
    "education": "Bakalavr",
    "education_speciality": "Kompüter elmləri",
    "facebook": "https://facebook.com/ali.valiyev",
    "instagram": "https://instagram.com/ali_valiyev",
    "tiktok": "",
    "linkedin": "",
    "profile_image": "Profil şəkli faylı (məsələn, image.jpg)",
    "work_images": ["İş şəkli 1 (məsələn, work1.jpg)", "İş şəkli 2 (məsələn, work2.jpg)"],
    "note": "Əlavə qeyd"
}

class RegisterAPIView(APIView):
    @swagger_auto_schema(
        request_body=register_request_body,
        operation_description="User registration endpoint",
        consumes=['multipart/form-data'],
        responses={201: openapi.Response(description='Qeydiyyat tamamlandı')},
        examples={
            'multipart/form-data': register_form_data_example
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"detail": "Qeydiyyat uğurla tamamlandı."}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
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