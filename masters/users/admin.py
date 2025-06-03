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


# from django.utils.html import format_html
# from django.contrib import admin
# from .models import CustomUser, WorkImage

# class WorkImageInline(admin.TabularInline):
#     model = CustomUser.work_images.through
#     extra = 0
#     verbose_name = "İş şəkli"
#     verbose_name_plural = "İş şəkilləri"

# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'mobile_number')
#     inlines = [WorkImageInline]

#     def work_images_preview(self, obj):
#         images = obj.work_images.all()
#         html = ""
#         for img in images:
#             if img.image:
#                 html += f'<a href="{img.image.url}" target="_blank"><img src="{img.image.url}" width="100" style="margin:2px"/></a>'
#         return format_html(html)
#     work_images_preview.short_description = "İş şəkilləri"

#     readonly_fields = ['work_images_preview']

#     fieldsets = (
#         (None, {
#             'fields': ('first_name', 'last_name', 'mobile_number', 'work_images_preview', 'is')
#         }),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)
