from django.db import models
from django.utils import timezone
from django.db.models import Avg
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from ..validators import azerbaijani_letters_validator, mobile_number_validator
from ..user_managers import CustomUserManager

from services.models.category_model import Category
from services.models.service_model import Service
from reviews.models.review_models import Review
from core.models.city_model import City
from core.models.language_model import Language



class CustomUser(AbstractBaseUser, PermissionsMixin):
    ##########//  Şəxsi məlumatlar  \\##########
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
        ('MALE', 'Kişi'),
        ('FEMALE', 'Qadın')
    ]
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        verbose_name="Cins"
    )


    ##########//  Peşə məlumatları  \\##########
    profession_area = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='category_masters'
    )

    profession_speciality = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='profession_masters'
    )

    experience_years = models.PositiveIntegerField(
        verbose_name="İş təcrübəsi (il ilə)"
    )

    custom_profession = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    cities = models.ManyToManyField(
        City,
        related_name='city_masters',
        verbose_name='Şəhərlər',
    )

    ##########//  Təhsil məlumatları  \\##########
    EDUCATION_CHOICES = [
        ('0', 'Yoxdur'),
        ('1', 'Tam ali'),
        ('2', 'Natamam ali'),
        ('3', 'Orta'),
        ('4', 'Peşə təhsili'),
        ('5', 'Orta ixtisas təhsili'),
    ]
    education = models.CharField(
        max_length=20,
        choices=EDUCATION_CHOICES,
        verbose_name="Təhsil səviyyəsi"
    )

    education_speciality = models.CharField(
        max_length=50,
        blank=True,
        validators=[azerbaijani_letters_validator],
        verbose_name="Təhsil üzrə ixtisas"
    )

    languages = models.ManyToManyField(
        Language,
        verbose_name="Bildiyi dillər"
    )

    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        verbose_name="Profil şəkli"
    )

    facebook = models.URLField(blank=True, verbose_name="Facebook linki")
    instagram = models.URLField(blank=True, verbose_name="Instagram linki")
    tiktok = models.URLField(blank=True, verbose_name="TikTok linki")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn linki")

    work_images = models.ManyToManyField(
        "WorkImage",
        blank=True,
        verbose_name="İşlərinə aid şəkillər"
    )

    note = models.TextField(
        blank=True,
        max_length=1500,
        verbose_name="Əlavə qeyd"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Yaradılma tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son yenilənmə tarixi")

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = [] 

    objects = CustomUserManager()

    def average_rating(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('rating'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def average_responsible(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('responsible'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def average_neat(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('neat'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def average_time_management(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('time_management'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def average_communicative(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('communicative'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def average_punctual(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('punctual'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def average_professional(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('professional'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def average_experienced(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('experienced'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def average_efficient(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('efficient'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def average_agile(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('agile'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def average_patient(self):
        average = Review.objects.filter(master=self).aggregate(avg=Avg('patient'))['avg']
        if average is None:
            return ''
        return round(average, 2)

    @property
    def review_count(self):
        return Review.objects.filter(master=self).count()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.mobile_number})"