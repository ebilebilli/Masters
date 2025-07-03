import logging
import uuid
from django.conf import settings
import redis
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from drf_yasg.utils import swagger_auto_schema

from users.tasks import send_otp_task
from users.serializers.password_serializers import (
    PasswordResetConfirmSerializer,
    VerifyOTPSerializer, 
    PasswordResetRequestSerializer
)
from utils.otp import (
    check_otp_in_redis, 
    delete_otp_in_redis, 
    get_mobile_number_by_otp_in_redis
)


logger = logging.getLogger(__name__)

__all__ = [
    'PasswordResetRequestAPIView',
    'VerifyOTPAPIView',
    'PasswordResetConfirmAPIView'
]

class PasswordResetRequestAPIView(APIView):
    """
    API endpoint to send an OTP to the user's mobile number for password reset.

    Accepts a mobile number, validates it, and sends an OTP via a background task (or directly).
    Designed to initiate the password reset process.

    Permissions: AllowAny (no authentication required)
    Method: POST
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
                send_otp_task.delay(serializer.validated_data['mobile_number'])  
                serializer.save()
                return Response({'message': 'OTP göndərildi.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'OTP göndərilə bilmədi: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPAPIView(APIView):
    """
    API endpoint to verify the OTP sent to the user's mobile number.

    Accepts an OTP code, validates it with Redis or temporary storage,
    and returns a temporary token if verification is successful.

    Permissions: AllowAny
    Method: POST
    """
    permission_classes = [AllowAny]
    http_method_names = ['post']

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        responses={
            200: 'OTP yoxlaması uğurludur',
            400: 'Yanlış OTP kod',
            500: 'OTP yoxlanıla bilmədi'
        }
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp_code']
            try:
                mobile_number = get_mobile_number_by_otp_in_redis(otp_code)
                check_otp_in_redis({'otp_code': otp_code, 'mobile_number': mobile_number})
                token = str(uuid.uuid4())
                settings.REDIS_CLIENT.setex(f'token:{token}', 300, mobile_number)
                delete_otp_in_redis({'otp_code': otp_code, 'mobile_number': mobile_number})
                return Response({'message': 'OTP yoxlaması uğurludur', 'token': token}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'OTP yoxlanıla bilmədi: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    """
    API endpoint to confirm password reset using a temporary token.

    Accepts a new password and token, verifies the token,
    and updates the user's password accordingly.

    Permissions: AllowAny
    Method: POST
    """
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
        serializer = PasswordResetConfirmSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({'message': 'Parol uğurla dəyişdirildi.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f'Parol dəyişdirilə bilmədi: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)