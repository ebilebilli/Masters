import uuid
from django.conf import settings
import redis
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models.user_model import CustomUser


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

    def save(self):
        mobile_number = self.context['mobile_number']
        new_password = self.validated_data['new_password']
        user = CustomUser.objects.get(mobile_number=mobile_number)
        user.set_password(new_password)
        user.save()
        auth_header = self.context['request'].headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else auth_header
        settings.REDIS_CLIENT.delete(f'token:{token}')
        return user