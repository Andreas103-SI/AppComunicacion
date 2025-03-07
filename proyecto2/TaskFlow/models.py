from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import datetime


    
class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('member', 'Miembro'),
        ('guest', 'Invitado'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='member')

    def __str__(self):
        return self.username

        
class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Proyecto(models.Model):
    ESTADOS = (
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='proyectos')
    
    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    )

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_limite = models.DateField()
    fecha_vencimiento = models.DateField(default=datetime.date.today) #Se agrego este campo
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    usuarios_asignados = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tareas')
    asignado_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True) #Se agrego este campo

    def __str__(self):
        return self.nombre

        
class Grupo(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='grupos')
    proyecto = models.ForeignKey(
        'Proyecto',
        on_delete=models.CASCADE,
        related_name='grupos',
        null=True,  # Permite nulos
        blank=True  # Permite formularios sin este campo
    )

    def __str__(self):
        return self.nombre

class Mensaje(models.Model):
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    usuario_emisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensajes_enviados'
    )
    usuario_receptor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensajes_recibidos',
        null=True,
        blank=True
    )
    grupo = models.ForeignKey(
        Grupo,
        on_delete=models.CASCADE,
        related_name='mensajes',
        null=True,
        blank=True
    )

    def __str__(self):
        receptor = self.usuario_receptor if self.usuario_receptor else "Grupo"
        return f"De {self.usuario_emisor} para {receptor}: {self.contenido[:30]}"

class Comentario(models.Model):
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )
    
    def __str__(self):
        return f"Comentario de {self.usuario} en {self.tarea}"

class Notificacion(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    
    def __str__(self):
        estado = "Leída" if self.leida else "No leída"
        return f"Notificación para {self.usuario} - {estado}"

class Mensaje(models.Model):
    remitente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.remitente} a {self.destinatario}: {self.contenido[:20]}'

