from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name='loginUser'),  
    path('logout/<int:idUser>', views.logoutUser, name='logoutUser'),  
    path('subirTarea/<int:idUser>', views.subirTarea, name='subirTarea'),  
    path('darTarea/<int:idUser>', views.darTarea, name='darTarea'),  
    path('chatear/<int:idUser>/<int:idDocente>', views.chatear, name='chatear'),  
    # path('signin/', views.signinUser, name='signin'),
    # path('obtenerDatos/', views.signinUser, name='signin'),  
]