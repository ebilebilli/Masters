from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from apis.user_apis.register_views import *
from apis.user_apis.profile_views  import *
from apis.user_apis.master_views import *
from apis.user_apis.master_img_views import *
from apis.user_apis.register_views import LogoutAPIView


app_name = 'user_apis'

urlpatterns = [            
    # Master endpoints
    path(
        'professionals/', 
        MastersListAPIView.as_view(), 
        name='professionals-list'
    ),
    path(
        'professionals/top/', 
        TopRatedMastersListAPIView.as_view(), 
        name='professionals-top-rated-list '
    ),
    path(
        'professionals/<int:master_id>/', 
        MasterDetailAPIView.as_view(),
        name='professionals-detail'
    ),
    path(
        'professionals/<int:master_id>/delete', 
        MasterProfileDeleteAPIView.as_view(),
        name='professionals-delete'
    ),  
    
    #Master handwork images endpoints
    path(
        'professionals/<int:master_id>/images/',
        WorkImagesForMasterAPIView.as_view(),
        name='work-images'
    ),
    path(
        'professionals/images/create/',
        CreateWorkImagesForMasterAPIView.as_view(),
        name='create-image'
    ),
    path(
        'professionals/images/delete/',
        DeleteMasterWorkImageAPIView.as_view(),
        name='delete-image'
    ),
    
    #Auth views
    path(
        'register/',
        RegisterAPIView.as_view(),
        name='register'
    ),
    path(
        'login/', 
        LoginAPIView.as_view(), 
        name='login'
    ),
    path(
        'logout/', 
        LogoutAPIView.as_view(), 
        name='logout'
    ),
    path(
        'profile/', 
        ProfileAPIView.as_view(), 
        name='profile'
    ),
    path(
        'update/', 
        ProfileUpdateAPIView.as_view(), 
        name='update'
    ),
    path(
        'profile/delete/',
        ProfileDeleteAPIView.as_view(),
        name='profile-delete'
    ),
    path(
        'test/',
        TestAPIView.as_view(),
        name='test'
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