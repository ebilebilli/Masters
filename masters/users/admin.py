from django.contrib import admin

from .models.user_models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'is_master', 'first_name', 'last_name')
    search_fields = ('phone_nnumber',)
    list_per_page = 20
