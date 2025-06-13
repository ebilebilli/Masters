from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser
from .models.work_image_model import WorkImage


@admin.register(WorkImage)
class WorkImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    search_fields = ['field_name']
    list_per_page = 20



@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = (
        'first_name', 'last_name', 'mobile_number', 'gender', 'profession_area', 'experience_years', 'is_staff'
    )
    list_filter = ('gender', 'profession_area', 'is_active', 'is_staff')

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'birth_date', 'mobile_number', 'gender')
        }),
        ('Professional Information', {
            'fields': ('profession_area', 'profession_speciality', 'custom_profession', 'experience_years', 'cities', 'districts')
        }),
        ('Education and Languages', {
            'fields': ('education', 'education_speciality', 'languages')
        }),
        ('Additional Information', {
            'fields': ('profile_image', 'facebook', 'instagram', 'tiktok', 'linkedin', 'work_images', 'note')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('History', {
            'fields': ('last_login', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'password', 'is_active', 'is_staff', 'is_superuser')
        }),
    )

    search_fields = ('mobile_number', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('last_login', 'created_at', 'updated_at')