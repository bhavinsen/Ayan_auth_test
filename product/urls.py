from django.contrib import admin
from django.urls import path
from .views import ProductView

urlpatterns = [
    path('product/', ProductView.as_view(), name='rest_register'),
    path('product/<int:id>/', ProductView.as_view(), name='rest_register'),
]