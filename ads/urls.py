from django.urls import path

from .views import AdsList, AdDetail, AdCreate, AdUpdate, upload_file

urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),
    path('<int:pk>/', AdDetail.as_view(), name='ad_detail'),
    path('create/', AdCreate.as_view(), name='ad_create'),
    path('<int:pk>/update/', AdUpdate.as_view(), name='ad_update'),
    path('file-upload/', upload_file, name='file_upload')
]
