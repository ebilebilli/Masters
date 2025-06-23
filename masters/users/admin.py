from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from django.utils.translation import gettext_lazy as _

from .models import CustomUser
from .models.work_image_model import WorkImage


@admin.register(WorkImage)
class WorkImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    search_fields = ['field_name']
    list_per_page = 20
    

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'id', 'first_name', 'last_name', 'mobile_number',
        'gender', 'profession_area', 'experience_years',
        'is_active', 'is_staff', 'is_master',
    )
    list_filter = ('is_active', 'is_staff', 'is_master', 'gender', 'profession_area')
    search_fields = ('first_name', 'last_name', 'mobile_number')
    ordering = ('-created_at',)
    filter_horizontal = ('cities', 'districts', 'languages', 'work_images', 'groups', 'user_permissions')

    # Mövcud istifadəçini redaktə etmək üçün sahələr
    fieldsets = (
        (_("Şəxsi məlumatlar"), {
            "fields": (
                'first_name', 'last_name', 'birth_date', 'mobile_number', 'gender',
                'profile_image', 'note'
            )
        }),
        (_("Peşə məlumatları"), {
            "fields": (
                'profession_area', 'profession_speciality', 'experience_years',
                'custom_profession', 'cities', 'districts', 'work_images'
            )
        }),
        (_("Təhsil məlumatları"), {
            "fields": (
                'education', 'education_speciality', 'languages',
            )
        }),
        (_("Sosial şəbəkələr"), {
            "fields": (
                'facebook', 'instagram', 'tiktok', 'linkedin'
            )
        }),
        (_("İcazələr"), {
            "fields": (
                'is_active', 'is_staff', 'is_master', 'is_superuser', 'groups', 'user_permissions',
            )
        }),
        (_("Tarixlər"), {
            "fields": ('last_login', 'created_at', 'updated_at'),
        }),
    )

    # Yeni istifadəçi yaradanda görünsün deyə bütün sahələri əlavə edirik
    add_fieldsets = (
        (_("Əsas məlumatlar"), {
            'classes': ('wide',),
            'fields': (
                'mobile_number', 'password1', 'password2',
                'first_name', 'last_name', 'birth_date', 'gender',
                'profile_image', 'note',
                'profession_area', 'profession_speciality', 'experience_years',
                'custom_profession', 'cities', 'districts', 'work_images',
                'education', 'education_speciality', 'languages',
                'facebook', 'instagram', 'tiktok', 'linkedin',
                'is_active', 'is_staff', 'is_master', 'is_superuser', 'groups', 'user_permissions',
            ),
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'last_login')
