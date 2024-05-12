from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Es necesario un email electrónico.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class UserN(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=50)
    user = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    
    is_staff = models.BooleanField(default=True)
    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = ['email', 'password']

    objects = UserManager()

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    nombre = models.CharField(max_length=30)
    activo = models.BooleanField()

    def __str__(self):
        return self.nombre


class Funcion(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField()

    def __str__(self):
        return self.nombre


class Iu(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField()

    def __str__(self):
        return self.nombre


class UserNRol(models.Model):
    user = models.ForeignKey(UserN, on_delete=models.PROTECT)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    fecha_activacion = models.DateField()
    desde = models.DateField()
    hasta = models.DateField()

    def __str__(self):
        return f"{self.user.nombre} - {self.rol.nombre}"


class RolFuncion(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    funcion = models.ForeignKey(Funcion, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.rol.nombre} - {self.funcion.nombre}"


class FuncionIU(models.Model):
    funcion = models.ForeignKey(Funcion, on_delete=models.PROTECT)
    iu = models.ForeignKey(Iu, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.funcion.nombre} - {self.iu.nombre}"

class Docente(UserN):
    grado_academico = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre
    
class Curso(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT)

    def __str__(self):
        return f"Curso {self.id_curso}"

class Estudiante(UserN):
    codigo_sis = models.IntegerField()

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    fecha_publicado = models.DateField()
    fecha_limite = models.DateField(null=True, blank=True)
    titulo = models.CharField(max_length=30, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.titulo

class Inscrito(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    
    class Meta:
        unique_together = ['estudiante', 'curso']
        

    def __str__(self):
        return f"{self.estudiante.nombre} - Curso {self.curso.id_curso}"

class Entrega(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.PROTECT)
    inscrito = models.ForeignKey(Inscrito, on_delete=models.PROTECT)
    fecha_hora = models.DateTimeField()

    def __str__(self):
        return f"Entrega de {self.tarea.titulo} por {self.inscrito.estudiante.nombre}"


class TipoArchivo(models.Model):
    formato = models.CharField(max_length=30)

    def __str__(self):
        return self.formato


class Archivo(models.Model):
    tipo_archivo = models.ForeignKey(TipoArchivo, on_delete=models.PROTECT)
    entrega = models.ForeignKey(Entrega, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    archivo = models.BinaryField()

    def __str__(self):
        return self.nombre


class Comentario(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.PROTECT)
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion
