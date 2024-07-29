from django.contrib import admin
from django.urls import path, include

from mychatapp import views

urlpatterns = [
    path('', views.register, name = 'register'),
    path('signin', views.signin, name = 'signin'),
    path('index', views.index, name = 'index'),
    path('find_friends', views.find_friends, name = 'find_friends'),
    path('friends/<str:pk>', views.detail, name = 'detail'),
    path('add_friend', views.add_friend, name = 'add_friend'),
    path('signout', views.signout, name = 'signout'),
]