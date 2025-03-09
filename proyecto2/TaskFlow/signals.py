from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tarea, Notificacion

@receiver(post_save, sender=Tarea)
def crear_notificacion_tarea(sender, instance, created, **kwargs):
    if created and instance.asignado_a:
        mensaje = f"Se te ha asignado la tarea '{instance.nombre}' en el proyecto '{instance.proyecto.nombre}'."
        Notificacion.objects.create(usuario=instance.asignado_a, mensaje=mensaje)