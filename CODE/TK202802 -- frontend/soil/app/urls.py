from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path("index",views.index,name='index'),
    path("about/",views.about,name='about'),
    path("soilprediction/",views.soilprediction,name="soilprediction"),
    path("croppredictiopn/",views.croppredictiopn,name="croppredictiopn"),
    path("plantprediction/",views.plantprediction,name="plantprediction"),
    path("result/",views.result,name="result"), 
    path('admin1', views.admin_panel, name='admin1'),
    path('user', views.view_user, name='user'),
    path('soil', views.soil_history, name='soil'),
    path('crop', views.crop_history, name='crop'),
    path('plant', views.plant_history, name='plant'),
    
]