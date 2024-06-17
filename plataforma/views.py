from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
import jwt

from tbd.settings import SECRET_KEY
from .models import *

from datetime import datetime


def loginUser(request):
    if request.method == 'GET': 
        return render(request, "index.html")
    else:
        username = request.POST.get('nombre')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  
        
        if user is not None:
            payload = {'user_id': user.id, 'username': user.nombre}
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            # login(request, user) #Solamente permite una sesion
            Session.objects.create(id_user=user, token=token, activo=True)
            
            res = obtener_iu_para_usuario(user.id)
            interfaces_nombre = []
                
            for elemento in res:
                interfaces_nombre.append(elemento.nombre)

            return render(request, 'signin.html', {'interfaces': interfaces_nombre, 'datosUsuario':{'id': user.id, 'nombre': user.nombre, 'token': token}})
        else:
            error_message = 'Usuario o contraseña incorrectos'
            return render(request, 'index.html', {'error': error_message})
        
def logoutUser(request, idUser):
    sesion = Session.objects.filter(id_user=idUser, activo=True).first()
    if(sesion):
        sesion.activo = False
        sesion.save()
    return redirect('loginUser')
    
##CONSULTAS    

def obtener_iu_para_usuario(user_id):
    ius = Iu.objects.filter(funcioniu__funcion__rolfuncion__rol__usernrol__user_id=user_id)
    return ius

def obtener_cursos(user_id):
    consultaRes = Curso.objects.filter(docente=user_id)
    return consultaRes   

def establecer_tarea(curso, fecha_publicado, fecha_limite, titulo, descripcion):
    Tarea.objects.create(curso = curso, fecha_publicado = fecha_publicado, fecha_limite = fecha_limite, titulo = titulo, descripcion =  descripcion)
    
def obtenerTareasAsignadas(idUser):
    tareasAsignadas = Tarea.objects.filter(curso__inscrito__estudiante_id=idUser).order_by('-id')
    return tareasAsignadas
    

##INTERFACES

def darTarea(request, idUser):
    if request.method == 'GET':
        cursos = obtener_cursos(idUser)
        return render(request, 'darTarea.html', {'idUser': idUser, 'cursos': cursos})
    else:
        fecha_actual = datetime.now()
        idCurso = int(request.POST.get('curso'))
        curso = Curso.objects.get(id=idCurso)
        fecha_publicado = fecha_actual
        fecha_limite = request.POST.get('limite')
        titulo = request.POST.get('titulo')
        descripcion =  request.POST.get('descripcion')
        
        establecer_tarea(curso, fecha_publicado, fecha_limite, titulo, descripcion)
        
        cursos = obtener_cursos(idUser)
        
        return render(request, 'darTarea.html', {'idUser': idUser, 'cursos': cursos})
    
def subirTarea(request, idUser):    
    tareasAsignadas = obtenerTareasAsignadas(idUser)
    return render(request, 'subirTarea.html', {'idUser':idUser, 'tareas':tareasAsignadas})

def chatear(request, idUser, idDocente):    
    return render(request, 'chat.html', {'idUser':idUser, 'idDocente':idDocente})

    

    
    


