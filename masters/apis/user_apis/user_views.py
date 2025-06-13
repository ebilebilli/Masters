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


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="İstifadəçi qeydiyyat üçün məlumatlar daxil edilir",
        request_body=RegisterSerializer(),
        responses={201: RegisterSerializer(), 400: 'Validasiya xətası'}
    )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            print("REQUEST GƏLDİ")
            try:
                user = serializer.save()
                return Response({
                    "message": "İstifadəçi uğurla yaradıldı.",
                    "user": {
                        "id": user.id,
                        "full_name": f"{user.first_name} {user.last_name}",
                        "mobile_number": user.mobile_number
                    }
                }, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"detail": "Gözlənilməz bir xəta baş verdi."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user:
            return Response({'mobile_number': user.mobile_number,
                            'first_name': user.first_name})
        else:
            return Response({'detal': 'ok'})
        


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
