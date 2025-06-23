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
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from users.serializers.user_serializers import(
    MobileNumberSerializer,
    RegisterSerializer,
    LoginSerializer,
)
from rest_framework.generics import CreateAPIView

from users.serializers.work_image_serializers import WorkImageSerializer
from users.models import WorkImage, CustomUser


class WorkImageCreateAPIView(CreateAPIView):
    queryset = WorkImage.objects.all()
    serializer_class = WorkImageSerializer


work_images_field = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(type=openapi.TYPE_FILE, format='binary'),
    description="İş şəkilləri (bir neçə fayl)",
    nullable=True,
)


class MobileNumberCheckAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="Mobil nömrəni yoxla",
        operation_description="Mobil nömrənin yalnız rəqəmlərdən ibarət olub-olmadığını və operator prefix-nin düzgünlüyünü yoxlayır.",
        examples=[
            OpenApiExample(
                name="Doğru format",
                value={"mobile_number": "501234567"},
                request_only=True
            )
        ],
        request=MobileNumberSerializer,
        responses={
            201: openapi.Response(description='Uğurlu qeydiyyat'),
            400: openapi.Response(description='Validasiya xətası')
        }
    )
    def post(self, request):
        serializer = MobileNumberSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            openapi.Parameter('cities', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="Şəhərlərin ID-ləri", collectionFormat='multi', required=False),
            openapi.Parameter('districts', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="Bakı ərazi ID-ləri", collectionFormat='multi', required=False),
            openapi.Parameter('languages', openapi.IN_FORM, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="Dillərin ID-ləri", collectionFormat='multi', required=True),
            openapi.Parameter('profession_area', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description="Peşə sahəsi ID", required=True),
            openapi.Parameter('profession_speciality', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Peşə ixtisası", required=True),
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
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

        return Response({"detail": "Qeydiyyat uğurla tamamlandı.", 'token': tokens}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
