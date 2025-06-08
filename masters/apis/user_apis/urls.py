from django.urls import path

from . import views as users_views


urlpatterns = [
    path('register/', users_views.RegisterAPIView.as_view(), name='register'),
    path('login/', users_views.LoginAPIView.as_view(), name='login'),
    path('update/', users_views.ProfileUpdateAPIView.as_view(), name='update'),
    path('test/', users_views.TestAPIView.as_view(), name='test'),
]
