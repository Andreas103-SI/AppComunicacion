from django.urls import path
from .views import ProyectoListView, ProyectoCreateView

urlpatterns = [
    path('proyectos/', ProyectoListView.as_view(), name='proyectos'),
    path('proyectos/crear/', ProyectoCreateView.as_view(), name='proyectos_crear'),
    path('proyectos/editar/<int:pk>/', ProyectoUpdateView.as_view(), name='proyectos_editar'),
    
]