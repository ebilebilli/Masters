from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers.profile_serializers import ProfileSerializer


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="İstifadəçi profil məlumatlarının gətirilməsi",
        responses={
            200: openapi.Response(
                description="İstifadəçi profil məlumatları",
                schema=ProfileSerializer()
            ),
            403: "Bu səhifə əlçatan deyil",
            401: "Avtorizasiya tələb olunur"
        }
    )

    def get(self, request):
        if request.user == request.user:
            serializer = ProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Məlumat': 'Bu səhifə əlçatan deyil'}, status=status.HTTP_403_FORBIDDEN)
        


# class ProfileUpdateAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def patch(self, request):
#         user = request.user
#         serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProfileUpdateAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     def put(self, request):
#         user = request.user
#         serializer = ProfileUpdateSerializer(instance=user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  