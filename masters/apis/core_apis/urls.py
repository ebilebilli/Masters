from django.urls import path

from apis.core_apis.city_views import *
from apis.core_apis.language_views import *


app_name = 'core_apis'

urlpatterns = [
    #City endpoints
    path(
        'cities/',
        CityListAPIView.as_view(),
        name='cities'
    ),
    #Language endpointss
    path(
        'languages/',
        LanguageListAPIView.as_view(),
        name='languages'
    )
]