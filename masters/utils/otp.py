import redis
from django.core.exceptions import ValidationError
from django.conf import settings
from random import choices


def create_otp(mobile_number):
    #code = ''.join(choices('0123456789', k=6))
    code = 111111   #it is default code for development

    redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
    redis_key = f'otp:{mobile_number}'
    redis_client.setex(redis_key, 180, code)

    return code


def get_mobile_number_by_otp_in_redis(otp_code):
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
    for key in redis_client.scan_iter(match='otp:*'):
        stored_code = redis_client.get(key)
        if stored_code and stored_code.decode('utf-8') == otp_code:
            return key.decode('utf-8').split(':')[1]
    return None


def check_otp_in_redis(data):
    redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
    redis_key = f"otp:{data['mobile_number']}"
    stored_code = redis_client.get(redis_key)

    if not stored_code or stored_code.decode('utf-8') != data['otp_code']:
        raise ValidationError({'otp_code': 'Yanlış və ya vaxtı keçmiş OTP kodu.'})


def delete_otp_in_redis(data):
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
        )
    redis_client.delete(f'otp:{data["mobile_number"]}')
