from .models import Notificacion

def notificaciones_no_leidas(request):
    if request.user.is_authenticated:
        notificaciones = Notificacion.objects.filter(usuario=request.user, leida=False).count()
    else:
        notificaciones = 0
    return {'notificaciones_no_leidas': notificaciones}