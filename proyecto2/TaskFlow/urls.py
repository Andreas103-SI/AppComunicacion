from django.urls import path
from .views import (
    ProyectoListView, ProyectoCreateView, ProyectoUpdateView, ProyectoDeleteView, ProyectoDetailView,
    TareaListView, TareaCreateView, TareaUpdateView, TareaDeleteView,
    MensajeListView, ComentarioCreateView, NotificacionesView, marcar_notificacion_leida,
    home_view
)

urlpatterns = [
    # Página de inicio
    path('', home_view, name='home'),
    
    # Proyectos
    path('proyectos/', ProyectoListView.as_view(), name='proyectos'),
    path('proyectos/crear/', ProyectoCreateView.as_view(), name='proyectos_crear'),
    path('proyectos/<int:pk>/editar/', ProyectoUpdateView.as_view(), name='proyectos_editar'),
    path('proyectos/<int:pk>/eliminar/', ProyectoDeleteView.as_view(), name='proyectos_eliminar'),
    path('proyectos/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto_detalle'),
    
    # Tareas
    path('tareas/', TareaListView.as_view(), name='tareas'),
    path('proyectos/<int:proyecto_id>/tareas/', TareaListView.as_view(), name='tareas_proyecto'),
    path('proyectos/<int:proyecto_id>/tareas/crear/', TareaCreateView.as_view(), name='tarea_crear'),
    path('tareas/<int:pk>/editar/', TareaUpdateView.as_view(), name='tarea_editar'),
    path('tareas/<int:pk>/eliminar/', TareaDeleteView.as_view(), name='tarea_eliminar'),
    
    # Mensajes
    path('mensajes/', MensajeListView.as_view(), name='mensajes'),
    #path('mensajes/crear/', MensajeCreateView.as_view(), name='mensaje_crear'),

    # Comentarios
    path('tareas/<int:tarea_id>/comentarios/crear/', ComentarioCreateView.as_view(), name='comentario_crear'),
    
    # Notificaciones
    path('notificaciones/', NotificacionesView.as_view(), name='notificaciones'),
    path('notificaciones/<int:notificacion_id>/marcar-leida/', marcar_notificacion_leida, name='marcar_notificacion_leida'),
]