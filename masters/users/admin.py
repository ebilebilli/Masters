from django.contrib import admin

from .models.user_model import CustomUser



@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile_number')
    search_fields = ('mobile_number',)
    list_per_page = 20
