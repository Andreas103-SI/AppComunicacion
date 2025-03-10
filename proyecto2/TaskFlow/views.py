from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView #Agrega DetailView a la lista de importaciones.
from .models import Proyecto, Tarea, Comentario
from .forms import RegistroForm, ProyectoForm, ComentarioForm
from .mixins import AdminRequiredMixin
from .forms import TareaForm
from django.http import Http404
from django.shortcuts import render
from .models import Mensaje
from .models import Notificacion
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models



def home_view(request):
    return render(request, "home.html")

class CustomLoginView(LoginView):
    template_name = "login.html"

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")

class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = "registro.html"
    success_url = reverse_lazy("login")

class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyectos/proyecto_list.html'

class ProyectoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/proyecto_form.html'
    success_url = '/proyectos/'

class ProyectoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/proyecto_update.html'
    success_url = '/proyectos/'

class ProyectoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Proyecto
    success_url = reverse_lazy('proyectos')
    template_name = 'proyectos/proyecto_confirm_delete.html'

    def get_queryset(self):
        return Proyecto.objects.all()



class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'tareas/tarea_list.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        proyecto_id = self.kwargs.get('proyecto_id')
        print(f"Proyecto ID: {proyecto_id}")  # Depuración
        if proyecto_id:
            # Si es administrador, muestra todas las tareas del proyecto
            if self.request.user.is_superuser or self.request.user.is_staff:
                tareas = Tarea.objects.filter(proyecto_id=proyecto_id)
            else:
                # Para usuarios normales, muestra solo las tareas asignadas a ellos
                tareas = Tarea.objects.filter(
                    proyecto_id=proyecto_id
                ).filter(
                    models.Q(asignado_a=self.request.user) |
                    models.Q(usuarios_asignados=self.request.user)
                )
            print(f"Tareas encontradas: {list(tareas)}")  # Depuración
            return tareas
        return Tarea.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto_id = self.kwargs.get('proyecto_id')
        context['proyecto_id'] = proyecto_id
        context['proyecto'] = Proyecto.objects.get(id=proyecto_id)
        return context


class TareaCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/tarea_form.html'

    def form_valid(self, form):
        form.instance.proyecto = Proyecto.objects.get(id=self.kwargs['proyecto_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('proyecto_detalle', kwargs={'pk': self.kwargs['proyecto_id']})

class TareaUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/tarea_form.html'

    def get_success_url(self):
        return reverse_lazy('proyecto_detalle', kwargs={'pk': self.object.proyecto.id})

class TareaDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Tarea
    template_name = 'tareas/tarea_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('proyecto_detalle', kwargs={'pk': self.object.proyecto.id})


class ProyectoDetailView(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyectos/proyecto_detail.html'
    context_object_name = 'proyecto'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Proyecto.objects.all()
        return Proyecto.objects.filter(usuarios=self.request.user)

    def handle_no_permission(self):
        return render(self.request, 'proyectos/no_permission.html', {'message': 'No tienes permiso para acceder a la información de este proyecto.'})

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return self.handle_no_permission()


class MensajeListView(LoginRequiredMixin, ListView):
    model = Mensaje
    template_name = 'mensajes/mensaje_list.html'

    def get_queryset(self):
        return Mensaje.objects.filter(destinatario=self.request.user).order_by('-fecha')
    
    
class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentarios/comentario_form.html'

    def form_valid(self, form):
        form.instance.tarea = Tarea.objects.get(id=self.kwargs['tarea_id'])
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('proyecto_detalle', kwargs={'pk': self.object.tarea.proyecto.id})
    
    


class NotificacionesView(LoginRequiredMixin, ListView):
    model = Notificacion
    template_name = 'notificaciones/notificaciones.html'
    context_object_name = 'notificaciones'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Notificacion.objects.filter(leida=False).order_by('-fecha')
        return Notificacion.objects.filter(
            usuario=self.request.user,
            leida=False
        ).order_by('-fecha')
        

@login_required
def marcar_notificacion_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    if request.method == "POST":
        notificacion.leida = True
        notificacion.save()
    # Después de marcarla como leída, redirige a la vista de notificaciones
    return redirect('notificaciones')