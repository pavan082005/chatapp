from django.contrib import admin
from django.urls import path, include

from mychatapp import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('friends/<str:pk>', views.detail, name = 'detail')
]