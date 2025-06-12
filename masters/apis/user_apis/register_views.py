from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers.user_serializers import(
    RegisterSerializer,
    LoginSerializer,
    ProfileUpdateSerializer
)
from rest_framework.generics import CreateAPIView

from users.serializers.user_serializers import WorkImageSerializer
from users.models import WorkImage


class WorkImageCreateAPIView(CreateAPIView):
    queryset = WorkImage.objects.all()
    serializer_class = WorkImageSerializer


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser] 

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
        


class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)