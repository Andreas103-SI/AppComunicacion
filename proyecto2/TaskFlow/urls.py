from django.urls import path
from . import views
from .views import ProyectoListView, ProyectoCreateView, ProyectoUpdateView, ProyectoDeleteView, ProyectoDetailView
from .views import TareaListView, TareaCreateView, TareaUpdateView, TareaDeleteView
from .views import home_view, ProyectoListView



urlpatterns = [
    path('proyectos/', ProyectoListView.as_view(), name='proyectos'),
    path('proyectos/crear/', ProyectoCreateView.as_view(), name='proyectos_crear'),
    path('proyectos/editar/<int:pk>/', ProyectoUpdateView.as_view(), name='proyectos_editar'),
    path('proyectos/eliminar/<int:pk>/', ProyectoDeleteView.as_view(), name='proyectos_eliminar'),
    path('tareas/', TareaListView.as_view(), name='tareas'),
    path('proyectos/<int:proyecto_id>/tareas/crear/', TareaCreateView.as_view(), name='tarea_crear'),
    path('tareas/editar/<int:pk>/', TareaUpdateView.as_view(), name='tarea_editar'),
    path('tareas/eliminar/<int:pk>/', TareaDeleteView.as_view(), name='tarea_eliminar'),
    path('proyectos/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto_detalle'),
]