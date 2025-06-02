from django.contrib import admin

from .models.user_model import CustomUser
from .models.language_model import Language
from .models.work_image_model import WorkImage



@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_number', 'first_name', 'last_name', 'is_staff')
    search_fields = ('mobile_number',)
    list_per_page = 20



@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20



@admin.register(WorkImage)
class WorkImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    search_fields = ('image',)
    list_per_page = 20