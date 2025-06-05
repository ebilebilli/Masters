from django.urls import path, include


urlpatterns = [
    path('users/', include('apis.user_apis.urls')),
]