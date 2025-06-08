from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_superuser(self, phone_number, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_active_on_main_page', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser üçün is_staff=True olmalıdır.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser üçün is_superuser=True olmalıdır.')

        return self.create_user(phone_number, full_name, password, **extra_fields)    