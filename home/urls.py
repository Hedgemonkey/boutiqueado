from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('test_s3_connection/', views.test_s3_connection, name='test_s3_connection'),
]
