from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name='loginUser'),  
    path('logout/', views.logoutUser, name='logoutUser'),  
    path('signin/', views.signinUser, name='signin'),
    path('obtenerDatos/', views.signinUser, name='signin'),  
]