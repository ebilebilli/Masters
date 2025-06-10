from django.urls import path

from apis.review_apis.review_views import *


app_name = 'review_apis'

urlpatterns = [
    path(
        'professionals/<int:master_id>/reviews/',
        ReviewsForMasterAPIView.as_view(),
        name="professionals-reviews-list"
    ),
    
    path(
        'professionals/<int:master_id>/reviews/create/',
         CreateReviewAPIView.as_view(),
         name='create-reviews'
    ),

    path(
        'professionals/reviews/<int:review_id>/update/',
        UpdateReviewAPIView.as_view(),
        name='udpate-reviews'
    ),

    path(
        'professionals/reviews/<int:review_id>/delete/',
        DeleteReviewAPIView.as_view(),
        name='delete-reviews'
    ),

    path(
        'professionals/<int:master_id>/reviews/filter/',
        FilterReviewAPIView.as_view(),
        name='filter-reviews'
    )
]
