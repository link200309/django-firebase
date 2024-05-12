from django import urls
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import *
from rest_framework.authtoken.models import Token

def loginUser(request):
    if request.method == 'GET': 
        return render(request, "index.html")
    else:
        username = request.POST.get('nombre')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)  
        
        if user is not None:
            login(request, user) #Solamente permite una sesion
            
            return redirect('signin')
        else:
            error_message = 'Usuario o contraseña incorrectos'
            return render(request, 'index.html', {'error': error_message})
        
def logoutUser(request):
    logout(request)
    return redirect('loginUser')

def signinUser(request):
    user_id = None
    if request.user.is_authenticated:
        user_id = request.user.id
        res = obtener_iu_para_usuario(user_id)
        interfaces_nombre = []
        
        for elemento in res:
            interfaces_nombre.append(elemento.nombre)

        request.session.save()
        session_key = request.session.session_key    
        
            
    return render(request, 'signin.html', {'interfaces': interfaces_nombre, 'datosUsuario':{'id': user_id, 'nombre': request.user.nombre, 'token': session_key}})


def obtener_iu_para_usuario(user_id):
    print("INICIO OBTENER CREDENCIALES:")
    ius = Iu.objects.filter(funcioniu__funcion__rolfuncion__rol__usernrol__user_id=user_id)
    return ius
    


