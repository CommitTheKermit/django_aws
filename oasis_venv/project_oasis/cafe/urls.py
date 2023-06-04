from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #path('recommended', .as_view()),
    path('recommend', views.recommend_cafe)
]
