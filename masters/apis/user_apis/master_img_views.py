from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models.user_model import CustomUser
from users.models.work_image_model import WorkImage
from users.serializers.work_image_serializers import WorkImageSerializer
from utils.permissions import HeHasPermission

__all__ = [
    'WorkImagesForMasterAPIView',
    'DeleteMasterWorkImageAPIView'
]


class WorkImagesForMasterAPIView(APIView):
    """
    get:
    Retrieve a list of work images for a specific master.

    post:
    Upload one or more new work images for the authenticated master.
    Limits the total image count to 10.
    """
    permission_classes = [AllowAny]
    http_method_names = ['get']
    
    @swagger_auto_schema(
        operation_summary="Masterin iş şəkillərini göstər",
        responses={200: WorkImageSerializer(many=True)}
    )
    
    def get(self, request, master_id):
        master = get_object_or_404(CustomUser, id=master_id)
        images = master.work_images.all() 
        serializer = WorkImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteMasterWorkImageAPIView(APIView):
    """
    delete:
    Delete a master work image by its ID.

    Path Parameters:
    - image_id (int): The ID of the image to delete.

    Returns:
    - 204 No Content if deleted.
    - 400 Bad Request if image not found.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']
    
    @swagger_auto_schema(
    operation_summary="Şəkli sil",
    manual_parameters=[
        openapi.Parameter(
            'image_id',
            openapi.IN_PATH,
            description="Silinəcək şəklin ID-si",
            type=openapi.TYPE_INTEGER
        )
    ],
    responses={
        204: openapi.Response(description="Şəkil silindi"),
        400: openapi.Response(description="Şəkil tapılmadı"),
    }
    )
    def delete(self, request, image_id):
        try:
            image = WorkImage.objects.get(id=image_id)
            image.delete()
            return Response({'message': 'Şəkil silindi'}, status=status.HTTP_204_NO_CONTENT)
        except WorkImage.DoesNotExist:
            return Response({'error': 'Şəkil tapılmadı'}, status=status.HTTP_400_BAD_REQUEST)