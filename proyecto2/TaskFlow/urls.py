from django.urls import path
from . import views
from .views import ProyectoListView, ProyectoCreateView, ProyectoUpdateView, ProyectoDeleteView

urlpatterns = [
    path('proyectos/', ProyectoListView.as_view(), name='proyectos'),
    path('proyectos/crear/', ProyectoCreateView.as_view(), name='proyectos_crear'),
    path('proyectos/editar/<int:pk>/', ProyectoUpdateView.as_view(), name='proyectos_editar'),
    path('proyectos/eliminar/<int:pk>/', ProyectoDeleteView.as_view(), name='proyectos_eliminar'),
]