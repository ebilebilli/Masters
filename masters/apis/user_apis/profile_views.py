from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers.profile_serializers import ProfileSerializer

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user == request.user:
            serializer = ProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Məlumat': 'Bu səhifə əlçatan deyil'}, status=status.HTTP_403_FORBIDDEN)