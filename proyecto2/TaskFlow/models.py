from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('member', 'Miembro'),
        ('guest', 'Invitado'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='member')

    def __str__(self):
        return self.username

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
    # Relación muchos a muchos con Usuarios (definido mediante AUTH_USER_MODEL)
    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='proyectos')
    
    def __str__(self):
        return self.nombre
