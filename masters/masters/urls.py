from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from masters.settings import MEDIA_URL, MEDIA_ROOT

schema_view = get_swagger_view(title='TEST API')


urlpatterns = [
    path('api/', include('masters.api_routers')),

    path('admin/', admin.site.urls),
    path('test/', schema_view)
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)