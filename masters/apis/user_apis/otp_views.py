from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from drf_yasg.utils import swagger_auto_schema

from users.serializers.password_serializers import PasswordResetConfirmSerializer, PasswordResetRequestSerializer
from users.tasks import send_otp_task


__all__ = [
    'PasswordResetRequestAPIView',
    'PasswordResetConfirmAPIView'
]


class PasswordResetRequestAPIView(APIView):
    """
    API endpoint to request a password reset OTP via mobile number.
    Applies throttling to limit request rate.
    """
    permission_classes = [AllowAny]
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    http_method_names = ['post']
    
    @swagger_auto_schema(
        request_body=PasswordResetRequestSerializer,
        responses={
            200: 'OTP göndərildi',
            400: 'Yanlış məlumat',
            500: 'OTP göndərilə bilmədi'
        }
    )

    @transaction.atomic
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                send_otp_task(serializer.validated_data['mobile_number'])  #delay is not using yet because of server ram problems.In future it will solve
                serializer.save()
                return Response({'message': 'OTP göndərildi.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'OTP göndərilə bilmədi: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']
    
    @swagger_auto_schema(
        request_body=PasswordResetConfirmSerializer,
        responses={
            200: 'Parol uğurla dəyişdirildi',
            400: 'Yanlış məlumat',
            500: 'Parol dəyişdirilə bilmədi'
        }
    )

    @transaction.atomic
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'message': 'Parol uğurla dəyişdirildi.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'Parol dəyişdirilə bilmədi: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)