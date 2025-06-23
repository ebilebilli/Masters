from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from apis.user_apis.user_views import *
from apis.user_apis.profile_views  import *
from apis.user_apis.master_views import *
from apis.user_apis.master_img_views import *
from apis.user_apis.otp_views import *



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
        'check-phone/',
        MobileNumberCheckAPIView.as_view(),
        name='check-phone'
    ),
    path(
        'login/', 
        LoginAPIView.as_view(), 
        name='login'
    ),
    path(
        'profile/', 
        ProfileAPIView.as_view(), 
        name='profile'
    ),
    path(
        'profile/update/', 
        ProfileUpdateAPIView.as_view(), 
        name='profile-update'
    ),
    path(
        'profile/delete/', 
        ProfileDeleteAPIView.as_view(), 
        name='profile-delete'
    ),
    path(
        'logout/', 
        LogoutAPIView.as_view(), 
        name='logout'
    ),
 
    # OTP endpoints
    path(
        'password/reset/request/',
        PasswordResetRequestAPIView.as_view(),
        name='password-reset-request'  
    ),
    path(
        'password/otp/verify/',
        VerifyOTPAPIView.as_view(),
        name='verify-otp'
    ),
    path(
        'password/reset/confirm/',
        PasswordResetConfirmAPIView.as_view(),
        name='password-reset-confirm'
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