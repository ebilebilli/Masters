from django.contrib.auth.models import BaseUserManager
from django.utils import timezone



##########//  Custom User Manager  \\##########
class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError("Mobil nömrə mütləqdir.")
        extra_fields.setdefault("is_active", True)
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("first_name", "Admin")
        extra_fields.setdefault("last_name", "İstifadəçi")
        extra_fields.setdefault("birth_date", timezone.now().date())
        extra_fields.setdefault("gender", "MALE")
        extra_fields.setdefault("experience_years", 0)
        extra_fields.setdefault("education", "0")
        from services.models.category_model import Category
        from services.models.service_model import Service
        
        category, _ = Category.objects.get_or_create(name="Defolt Kateqoriya")
        service, _ = Service.objects.get_or_create(
            name="Defolt Xidmət",
            defaults={"category": category}  
        )
        extra_fields.setdefault("profession_area", category)
        extra_fields.setdefault("profession_speciality", service)

        return self.create_user(mobile_number, password, **extra_fields)