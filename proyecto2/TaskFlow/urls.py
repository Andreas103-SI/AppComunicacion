from django.urls import path
from .views import (
    home_view, ProyectoListView, ProyectoCreateView, ProyectoUpdateView, ProyectoDeleteView,
    TareaListView, TareaCreateView, TareaUpdateView, TareaDeleteView, ProyectoDetailView,
    MensajeListView, ComentarioCreateView, NotificacionesView, marcar_notificacion_leida,MensajeCreateView
)

urlpatterns = [
    path('', home_view, name='home'),
    path('proyectos/', ProyectoListView.as_view(), name='proyectos'),
    path('proyectos/crear/', ProyectoCreateView.as_view(), name='proyecto_crear'),
    path('proyectos/<int:pk>/editar/', ProyectoUpdateView.as_view(), name='proyecto_editar'),
    path('proyectos/<int:pk>/eliminar/', ProyectoDeleteView.as_view(), name='proyecto_eliminar'),
    path('proyectos/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto_detalle'),
    
    path('tareas/', TareaListView.as_view(), name='tareas'),
    path('proyectos/<int:proyecto_id>/tareas/', TareaListView.as_view(), name='tarea_list'),
    path('proyectos/<int:proyecto_id>/tareas/crear/', TareaCreateView.as_view(), name='tarea_crear'),
    path('tareas/<int:pk>/editar/', TareaUpdateView.as_view(), name='tarea_editar'),
    path('tareas/<int:pk>/eliminar/', TareaDeleteView.as_view(), name='tarea_eliminar'),
    
    path('mensajes/', MensajeListView.as_view(), name='mensajes'),
    path('tareas/<int:tarea_id>/comentarios/crear/', ComentarioCreateView.as_view(), name='comentario_crear'),
    path('mensajes/crear/', MensajeCreateView.as_view(), name='mensaje_crear'),


    path('notificaciones/', NotificacionesView.as_view(), name='notificaciones'),
    path('notificaciones/<int:notificacion_id>/marcar-leida/', marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('proyectos/<int:proyecto_id>/tareas/', TareaListView.as_view(), name='tarea_list'),
    path('proyectos/<int:proyecto_id>/tareas/crear/', TareaCreateView.as_view(), name='tarea_crear'),
    path('notificaciones/', NotificacionesView.as_view(), name='notificaciones'),
   
]