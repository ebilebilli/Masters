import redis
from django.core.exceptions import ValidationError
from django.conf import settings
from random import choices

def create_otp(mobile_number):
    code = '111111'  # İnkişaf üçün default kod
    redis_key = f'otp:{mobile_number}'
    settings.REDIS_CLIENT.setex(redis_key, 180, code)
    return code


def get_mobile_number_by_otp_in_redis(otp_code):
    for key in settings.REDIS_CLIENT.scan_iter(match='otp:*'):
        stored_code = settings.REDIS_CLIENT.get(key)
        if stored_code and stored_code == otp_code:
            return key.split(':')[1]
    return None


def check_otp_in_redis(data):
    redis_key = f"otp:{data['mobile_number']}"
    stored_code = settings.REDIS_CLIENT.get(redis_key)
    if not stored_code or stored_code != data['otp_code']:
        raise ValidationError({'otp_code': 'Yanlış və ya vaxtı keçmiş OTP kodu.'})


def delete_otp_in_redis(data):
    redis_key = f"otp:{data['mobile_number']}"
    settings.REDIS_CLIENT.delete(redis_key)