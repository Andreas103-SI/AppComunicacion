from django.db import models

from django.db import models
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

# Create your models here.
