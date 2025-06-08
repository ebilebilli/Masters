from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from apis.user_apis.register_views import *
from apis.user_apis.master_views import *
from apis.user_apis.master_img_views import *


app_name = 'user_apis'

urlpatterns = [            
    # Master endpoints
    path(
        'masters/', 
        MastersListAPIView.as_view(), 
        name='masters-list'
    ),
    path(
        'masters/top/', 
        TopRatedMastersListAPIView.as_view(), 
        name='masters-top-rated-list '
    ),
    path(
        'masters/<int:master_id>/', 
        MasterDetailAPIView.as_view(),
        name='master-detail'
    ),
    path(
        'masters/<int:master_id>/update', 
        MasterProfileUpdateAPIView.as_view(),
        name='master-update'
    ),  
    path(
        'masters/<int:master_id>/delete', 
        MasterProfileDeleteAPIView.as_view(),
        name='master-delete'
    ),  
    
    #Master handwork images endpoints
    path(
        'masters/<int:master_id>/images/',
        WorkImagesForMasterAPIView.as_view(),
        name='work-images'
    ),
    path(
        'masters/images/create/',
        CreateWorkImagesForMasterAPIView.as_view(),
        name='create-image'
    ),
    path(
        'masters/images/delete/',
        DeleteMasterWorkImageAPIView.as_view(),
        name='delete-image'
    ),
    
    #Jwt endpoints
    path(
        'api/token/', 
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]