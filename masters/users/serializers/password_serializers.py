import logging
import re
import uuid
from django.conf import settings
import redis
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models.user_model import CustomUser


logger = logging.getLogger(__name__)

__all__ = [
    'PasswordResetRequestSerializer',
    'VerifyOTPSerializer',
    'PasswordResetConfirmSerializer'
]


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer to handle password reset request via mobile number.

    Validates whether a user with the provided mobile number exists.
    """
    mobile_number = serializers.CharField(max_length=13, required=True)

    def validate_mobile_number(self, value):
        try:
            self._user = CustomUser.objects.get(mobile_number=value)
            return value
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'error': 'Bu telefon nömrəsi ilə istifadəçi tapılmadı.'})
            
    def save(self):
        return self._user


class VerifyOTPSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6, required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_two = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        auth_header = self.context['request'].headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else auth_header
        if not token:
            raise serializers.ValidationError({'error': 'Redis token tələb olunur.'})

        mobile_number = settings.REDIS_CLIENT.get(f'token:{token}')
        if not mobile_number:
            raise serializers.ValidationError({'token': 'Yanlış və ya vaxtı keçmiş token.'})
        
        mobile_number = mobile_number  
        self.context['mobile_number'] = mobile_number  

        if data['new_password'] != data['new_password_two']:
            raise serializers.ValidationError({'new_password': 'Şifrələr uyğun deyil.'})
        
        user = CustomUser.objects.get(mobile_number=mobile_number)
        validate_password(data['new_password'], user=user)
        return data

    def validate_new_password(self, value):
        if len(value) < 8 or len(value) > 16:
            raise serializers.ValidationError('Şifrəniz 8-16 simvol arası olmalı, böyük hərf, rəqəm və xüsusi simvol içərməlidir.')
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Şifrənizdə minimum bir böyük hərf olmalıdır.')
        if not re.search(r'\d', value):
            raise serializers.ValidationError('Şifrənizdə minimum bir rəqəm olmalıdır.')
        if not re.search(r'[!@#$%^&*()_\+\-=\[\]{};:"\\|,.<>\/?]', value):
            raise serializers.ValidationError('Şifrənizdə minimum bir xüsusi simvol olmalıdır.')
            
        return value

    def save(self):
        mobile_number = self.context['mobile_number']
        if isinstance(mobile_number, bytes):
            mobile_number = mobile_number.decode()
        logger.info(f"Redis-dən alınan mobil nömrə: {mobile_number}")

        try:
            user = CustomUser.objects.get(mobile_number=mobile_number)
        except CustomUser.DoesNotExist:
            logger.error(f"User tapılmadı: {mobile_number}")
            raise serializers.ValidationError({'user': 'İstifadəçi tapılmadı.'})

        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        logger.info(f"İstifadəçi {mobile_number} üçün yeni şifrə uğurla təyin edildi.")

        user.refresh_from_db()
        if user.check_password(new_password):
            logger.info("Yeni şifrə yoxlandı və doğrudur.")
        else:
            logger.error("Yeni şifrə bazaya düzgün yazılmayıb!")

        auth_header = self.context['request'].headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else auth_header
        settings.REDIS_CLIENT.delete(f'token:{token}')
        logger.info(f"Redis token {token} silindi.")

        return user