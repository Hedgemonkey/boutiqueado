from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('test_s3/', views.test_s3_connection, name='test_s3_connection'),
    path('upload_static/', views.upload_static_to_s3, name='upload_static_to_s3'),
]
