from django.contrib import admin
from .models import City, District


class CityAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name')
    search_fields = ('name', 'display_name')
    ordering = ('display_name',)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'city')
    search_fields = ('name', 'display_name')
    list_filter = ('city',)
    ordering = ('display_name',)


class EducationAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name')
    search_fields = ('name', 'display_name')
    ordering = ('display_name',)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name')
    search_fields = ('name', 'display_name')
    ordering = ('display_name',)


# Adminə qeydiyyat
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)

