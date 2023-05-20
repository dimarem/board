from django.urls import path

from .views import AdsList, AdDetail, AdCreate, AdUpdate, upload_file, left_feedback, FeedbacksList, FeedbackDelete, \
    accept_feedback

urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),
    path('<int:pk>/', AdDetail.as_view(), name='ad_detail'),
    path('create/', AdCreate.as_view(), name='ad_create'),
    path('<int:pk>/update/', AdUpdate.as_view(), name='ad_update'),
    path('file-upload/', upload_file, name='file_upload'),
    path('<int:pk>/feedback/', left_feedback, name='left_feedback'),
    path('feedbacks/', FeedbacksList.as_view(), name='feedbacks_list'),
    path('feedbacks/<int:pk>/delete/', FeedbackDelete.as_view(), name='feedback_delete'),
    path('feedbacks/<int:pk>/accept/', accept_feedback, name='feedback_accept')
]
