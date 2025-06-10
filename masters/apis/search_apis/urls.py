from django.urls import path
from apis.search_apis.search_views import SearchAPIView

app_name = 'search_apis'

urlpatterns = [
    path(
        'professionals/search/', 
        SearchAPIView.as_view(),
        name='professionals-search'
    ),
]