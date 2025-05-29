from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


# Yalnız Azərbaycan əlifbasındakı hərflərə icazə verilir (böyük və kiçik hərflər)
azerbaijani_letters_validator = RegexValidator(
    regex=r'^[A-Za-zƏəÖöĞğÜüÇçŞşİı]+$',
    message='Yalnız Azərbaycan əlifbasındakı hərflərə icazə verilir.'
)

# Mobil nömrə validatoru (9 rəqəm, məsələn: 501234567)
mobile_number_validator = RegexValidator(
    regex=r'^\d{9}$',
    message='Mobil nömrə düzgün daxil edilməyib. 50 123 45 67 formatında daxil edin.'
)


# class CustomUser(AbstractBaseUser):
#     name = models.CharField(
#         max_length=20,
#         validators=[azerbaijani_letters_validator],
#         verbose_name="Ad"
#     )
#     surname = models.CharField(
#         max_length=20,
#         validators=[azerbaijani_letters_validator],
#         verbose_name="Soyad"
#     )
#     birth_date = models.DateField(
#         verbose_name="Doğum tarixi",
#         help_text="Format: gün.ay.il (məsələn: 29.05.2025)",
#     )
#     models.CharField(
#         max_length=9,
#         validators=[phone_validator],
#         verbose_name="Mobil nömrə",
#     )


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError('Mobil nömrə daxil edilməlidir.')
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mobile_number, password, **extra_fields)

# User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=20,
        validators=[azerbaijani_letters_validator],
        verbose_name="Ad"
    )
    
    last_name = models.CharField(
        max_length=20,
        validators=[azerbaijani_letters_validator],
        verbose_name="Soyad"
    )

    birth_date = models.DateField(
        verbose_name="Doğum tarixi",
        help_text="Format: gün.ay.il (məsələn: 29.05.2025)"
    )

    mobile_number = models.CharField(
        max_length=9,
        unique=True,
        validators=[mobile_number_validator],
        verbose_name="Mobil nömrə"
    )

    GENDER_CHOICES = [
        ('K', 'Kişi'),
        ('Q', 'Qadın')
    ]

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Cins"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_date', 'gender']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.mobile_number}"