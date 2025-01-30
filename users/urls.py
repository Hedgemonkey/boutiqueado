from django.urls import path
from . import views

urlpatterns = [
    path('accounts2/login/', views.MyLoginView.as_view(), name='account_login'),
]
