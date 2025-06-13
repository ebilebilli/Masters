from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 

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
        'first_name', 'last_name', 'mobile_number', 'gender', 'profession_area',
        'profession_speciality', 'experience_years', 'education', 'is_active',
        'is_staff', 'created_at'
    )
    list_filter = ('gender', 'education', 'is_active', 'is_staff')
    search_fields = ('first_name', 'last_name', 'mobile_number')
    ordering = ('-created_at',)
    readonly_fields = ('last_login', 'created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('Şəxsi məlumatlar', {'fields': ('first_name', 'last_name', 'birth_date', 'gender')}),
        ('Peşə məlumatları', {'fields': ('profession_area', 'profession_speciality', 'experience_years', 'custom_profession', 'cities', 'districts')}),
        ('Təhsil məlumatları', {'fields': ('education', 'education_speciality', 'languages')}),
        ('Profil', {'fields': ('profile_image', 'facebook', 'instagram', 'tiktok', 'linkedin', 'work_images', 'note')}),
        ('İcazələr', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Tarixçə', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'first_name', 'last_name', 'birth_date', 'gender', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    filter_horizontal = ('cities', 'districts', 'languages', 'work_images', 'groups', 'user_permissions')