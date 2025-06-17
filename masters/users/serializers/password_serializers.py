from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models.user_model import CustomUser
from utils.otp import check_otp_in_redis, delete_otp_in_redis


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


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer to confirm password reset using OTP and set a new password.

    Validates OTP, ensures new passwords match, and applies Django's 
    password validation policy.
    """
    mobile_number = serializers.CharField(max_length=13, required=True)
    otp_code = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_two = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        if not CustomUser.objects.filter(mobile_number=data['mobile_number']).exists():
            raise serializers.ValidationError({'mobile_number': 'Bu telefon nömrəsi ilə istifadəçi tapılmadı.'})
        try:
            check_otp_in_redis(data)
        except Exception as e:
            raise serializers.ValidationError({'otp_code': f'OTP yoxlaması uğursuz: {str(e)}'})
        if data['new_password'] != data['new_password_two']:
            raise serializers.ValidationError({'new_password': 'Şifrələr uyğun deyil.'})
        user = CustomUser.objects.get(mobile_number=data['mobile_number'])
        validate_password(data['new_password'], user=user)
        return data
        
    def save(self):
        mobile_number = self.validated_data['mobile_number']
        new_password = self.validated_data['new_password']
        user = CustomUser.objects.get(mobile_number=mobile_number)
        user.set_password(new_password)
        user.save()
        delete_otp_in_redis(mobile_number)
        return user