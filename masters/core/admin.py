from django.contrib import admin
from .models.city_model import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('base_city__name',)
