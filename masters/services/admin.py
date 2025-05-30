from django.contrib import admin
from .models.service_model import Service
from .models.category_model import Category
from .models.service_model_image import ServiceImage


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'city', 'created_at')
    list_filter = ('city', 'category', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    inlines = [ServiceImageInline]
    filter_horizontal = ('category',)


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ('service', 'image', 'uploaded_at')
    search_fields = ('service__title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
