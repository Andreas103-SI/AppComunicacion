from django.urls import path
from .views import (
    # Vistas de Inicio
    home_view,

    # Vistas de Proyectos
    ProyectoListView,
    ProyectoCreateView,
    ProyectoDetailView,
    ProyectoUpdateView,
    ProyectoDeleteView,

    # Vistas de Tareas
    TareaListView,
    TareaCreateView,
    TareaDetailView,
    TareaUpdateView,
    TareaDeleteView,

    # Vistas de Comentarios y Notificaciones
    ComentarioCreateView,
    NotificacionesView,
    marcar_notificacion_leida,

    # Vistas de Mensajes
    MensajeListView,
    MensajeCreateView,
    MensajeReplyCreateView,
    MensajeDeleteView,
)

urlpatterns = [
    # Home
    path('', home_view, name='home'),

    # ---------------- PROYECTOS ----------------
    path('proyectos/', ProyectoListView.as_view(), name='proyectos'),
    path('proyectos/crear/', ProyectoCreateView.as_view(), name='proyecto_crear'),
    path('proyectos/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto_detalle'),
    path('proyectos/<int:pk>/editar/', ProyectoUpdateView.as_view(), name='proyecto_editar'),
    path('proyectos/<int:pk>/eliminar/', ProyectoDeleteView.as_view(), name='proyecto_eliminar'),

    # ---------------- TAREAS ----------------
    path('tareas/', TareaListView.as_view(), name='tareas'),
    path('tareas/<int:pk>/', TareaDetailView.as_view(), name='tarea_detalle'),
    path('tareas/<int:pk>/editar/', TareaUpdateView.as_view(), name='tarea_editar'),
    path('tareas/<int:pk>/eliminar/', TareaDeleteView.as_view(), name='tarea_eliminar'),
    path('proyectos/<int:proyecto_id>/tareas/', TareaListView.as_view(), name='tarea_list'),
    path('proyectos/<int:proyecto_id>/tareas/crear/', TareaCreateView.as_view(), name='tarea_crear'),

    # ---------------- COMENTARIOS ----------------
    path('tareas/<int:tarea_id>/comentarios/crear/', ComentarioCreateView.as_view(), name='comentario_crear'),

    # ---------------- MENSAJES ----------------
    path('mensajes/', MensajeListView.as_view(), name='mensajes'),  # Todos los mensajes (si aplica)
    path('mensajes/crear/', MensajeCreateView.as_view(), name='mensaje_crear'),

    # Mensajes por proyecto
    path('proyectos/<int:proyecto_id>/mensajes/', MensajeListView.as_view(), name='mensajes_proyecto'),
    path('proyectos/<int:proyecto_id>/mensajes/crear/', MensajeCreateView.as_view(), name='mensaje_crear_proyecto'),
    path('proyectos/<int:proyecto_id>/mensajes/<int:mensaje_id>/responder/', MensajeReplyCreateView.as_view(), name='mensaje_responder'),
    path('proyectos/<int:proyecto_id>/mensajes/<int:mensaje_id>/eliminar/', MensajeDeleteView.as_view(), name='mensaje_eliminar'),

    # ---------------- NOTIFICACIONES ----------------
    path('notificaciones/', NotificacionesView.as_view(), name='notificaciones'),
    path('notificaciones/<int:notificacion_id>/marcar-leida/', marcar_notificacion_leida, name='marcar_notificacion_leida'),
]
