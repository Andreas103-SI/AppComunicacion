from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView 
from .models import Proyecto, Tarea, Comentario
from .forms import RegistroForm, ProyectoForm, ComentarioForm, MensajeForm
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
    context_object_name = 'proyectos'

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Proyecto.objects.all()
        return Proyecto.objects.filter(usuarios=self.request.user)

class ProyectoDetailView(LoginRequiredMixin, DetailView):
    model = Proyecto
    template_name = 'proyectos/proyecto_detalle.html'
    context_object_name = 'proyecto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puedes agregar más contexto si lo necesitas (por ejemplo, tareas o mensajes del proyecto)
        return context

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
        if proyecto_id:
            proyecto = get_object_or_404(Proyecto, id=proyecto_id)
            if self.request.user.is_superuser or self.request.user.is_staff:
                return Tarea.objects.filter(proyecto_id=proyecto_id)
            elif self.request.user.is_authenticated:
                q1 = models.Q(asignado_a=self.request.user)
                q2 = models.Q(usuarios_asignados=self.request.user)
                return Tarea.objects.filter(proyecto_id=proyecto_id).filter(q1 | q2)
            else:
                return Tarea.objects.none()
        return Tarea.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto_id = self.kwargs.get('proyecto_id')
        context['proyecto_id'] = proyecto_id
        if proyecto_id:
            context['proyecto'] = get_object_or_404(Proyecto, id=proyecto_id)
        return context    

class TareaDetailView(DetailView):
    model = Tarea
    template_name = 'tarea_detalle.html'
    context_object_name = 'tarea'


class TareaCreateView(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/tarea_form.html'

    def form_valid(self, form):
        proyecto_id = self.kwargs.get('proyecto_id')
        if not proyecto_id:
            raise ValueError("No se proporcionó un proyecto_id en la URL.")
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        form.instance.proyecto = proyecto
        
        response = super().form_valid(form)
        
        tarea = self.object
        usuarios_notificados = set()  # Para evitar duplicados
        
        if tarea.asignado_a and tarea.asignado_a not in usuarios_notificados:
            Notificacion.objects.create(
                usuario=tarea.asignado_a,
                mensaje=f"Se te ha asignado la tarea '{tarea.nombre}' en el proyecto '{proyecto.nombre}'."
            )
            usuarios_notificados.add(tarea.asignado_a)
        
        for usuario in tarea.usuarios_asignados.all():
            if usuario not in usuarios_notificados:
                Notificacion.objects.create(
                    usuario=usuario,
                    mensaje=f"Has sido asignado a la tarea '{tarea.nombre}' en el proyecto '{proyecto.nombre}'."
                )
                usuarios_notificados.add(usuario)
        
        return response

    def get_success_url(self):
        proyecto_id = self.kwargs.get('proyecto_id')
        return reverse_lazy('tarea_list', kwargs={'proyecto_id': proyecto_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyecto_id'] = self.kwargs.get('proyecto_id')
        return context
                
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
    context_object_name = 'mensajes'

    def get_queryset(self):
        proyecto_id = self.kwargs.get('proyecto_id')
        if proyecto_id:
            # Filtra mensajes asociados al grupo del proyecto
            return Mensaje.objects.filter(
                models.Q(grupo__proyecto_id=proyecto_id) &
                (models.Q(usuario_receptor=self.request.user) | models.Q(usuario_emisor=self.request.user))
            ).order_by('-fecha_envio')
        return Mensaje.objects.filter(
            models.Q(usuario_receptor=self.request.user) | models.Q(usuario_emisor=self.request.user)
        ).order_by('-fecha_envio')
        
class MensajeCreateView(LoginRequiredMixin, CreateView):
    model = Mensaje
    form_class = MensajeForm
    template_name = 'mensajes/mensaje_form.html'
    success_url = reverse_lazy('mensajes')

    def form_valid(self, form):
        form.instance.usuario_emisor = self.request.user
        proyecto_id = self.kwargs.get('proyecto_id')  # Opcional, para mensajes relacionados con un proyecto
        if proyecto_id:
            proyecto = get_object_or_404(Proyecto, id=proyecto_id)
            grupo = proyecto.grupos.first()  # Toma el primer grupo del proyecto (ajusta según tu lógica)
            if grupo:
                form.instance.grupo = grupo
        return super().form_valid(form)

#Comentario


class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentarios/comentario_form.html'  # Ajusta la ruta según tu estructura

    def form_valid(self, form):
        tarea_id = self.kwargs.get('tarea_id')
        tarea = get_object_or_404(Tarea, id=tarea_id)
        form.instance.tarea = tarea
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        tarea_id = self.kwargs.get('tarea_id')
        return reverse_lazy('tarea_detalle', kwargs={'pk': tarea_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tarea_id = self.kwargs.get('tarea_id')
        context['tarea'] = get_object_or_404(Tarea, id=tarea_id)
        return context
        
#Notificaciones

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
    """
    Marca una notificación como leída y redirige a la lista de notificaciones.
    
    Args:
        request: La solicitud HTTP.
        notificacion_id (int): El ID de la notificación a marcar como leída.
    
    Retorna:
        HttpResponse: Redirige a la vista de notificaciones.
    """
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.leida = True
    notificacion.save()
    return redirect('notificaciones')