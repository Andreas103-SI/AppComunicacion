# Importaciones de Django
from django.db import models
from django.db.models import Q

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import Http404, HttpResponseRedirect

# Importaciones de vistas genéricas de Django
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

# Importaciones de TaskFlow
from .models import Proyecto, Tarea, Comentario, Mensaje, Notificacion, Grupo
from .forms import RegistroForm, ProyectoForm, ComentarioForm, MensajeForm, TareaForm
from .mixins import AdminRequiredMixin



# Vistas de Inicio

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


# Vista para detalles de proyecto
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


class ProyectoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Proyecto
    template_name = 'proyectos/proyecto_confirm_delete.html'
    success_url = reverse_lazy('proyectos')

    def test_func(self):
        # Solo el superusuario o el creador del proyecto puede eliminarlo
        proyecto = self.get_object()
        return self.request.user.is_superuser or (hasattr(proyecto, 'creador') and proyecto.creador == self.request.user)

    def handle_no_permission(self):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tienes permiso para eliminar este proyecto.")



# Vistas de Tareas

class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'tareas/tarea_list.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        proyecto_id = self.kwargs.get('proyecto_id')
        if proyecto_id:
            proyecto = get_object_or_404(Proyecto, id=proyecto_id)
            if self.request.user.is_superuser or self.request.user.is_staff:
                return Tarea.objects.filter(proyecto_id=proyecto_id).prefetch_related('comentarios')
            elif self.request.user.is_authenticated:
                q1 = models.Q(asignado_a=self.request.user)
                q2 = models.Q(usuarios_asignados=self.request.user)
                return Tarea.objects.filter(proyecto_id=proyecto_id).filter(q1 | q2).prefetch_related('comentarios')
            else:
                return Tarea.objects.none()
        return Tarea.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto_id = self.kwargs.get('proyecto_id')
        if proyecto_id:
            context['proyecto'] = get_object_or_404(Proyecto, id=proyecto_id)
        return context


class TareaDetailView(LoginRequiredMixin, DetailView):
    model = Tarea
    template_name = 'tareas/tarea_detalle.html'
    context_object_name = 'tarea'



class TareaCreateView(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/tarea_form.html'

    def form_valid(self, form):
        proyecto_id = self.kwargs.get('proyecto_id')
        
        # Si no se encuentra proyecto_id, redirige o muestra un mensaje
        if not proyecto_id:
            return redirect('proyectos')  # O podrías redirigir a alguna página de error
            
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        form.instance.proyecto = proyecto
        
        # Validación del formulario
        response = super().form_valid(form)
        
        tarea = self.object
        usuarios_notificados = set()

        # Notificaciones a los usuarios asignados
        if tarea.asignado_a and tarea.asignado_a not in usuarios_notificados:
            Notificacion.objects.create(
                usuario=tarea.asignado_a,
                mensaje=f"Se te ha asignado la tarea '{tarea.nombre}' en el proyecto '{proyecto.nombre}'."
            )
            usuarios_notificados.add(tarea.asignado_a)
        
        # Notificación a otros usuarios asignados
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
        if not proyecto_id:
            return reverse_lazy('proyectos')  # O redirige a alguna página si no existe el proyecto_id
        return reverse_lazy('tarea_list', kwargs={'proyecto_id': proyecto_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyecto_id'] = self.kwargs.get('proyecto_id')
        return context

# Vista para editar una tarea
class TareaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/tarea_form.html'

    def test_func(self):
        # Solo superusuarios o staff pueden editar tareas
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyecto_id'] = self.object.proyecto.id
        return context

    def get_success_url(self):
        messages.success(self.request, "Tarea actualizada correctamente.")
        return reverse_lazy('tarea_list', kwargs={'proyecto_id': self.object.proyecto.id})

# Vista para eliminar una tarea
class TareaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tarea
    template_name = 'tareas/tarea_confirm_delete.html'

    def test_func(self):
        # Solo superusuarios o staff pueden eliminar tareas
        return self.request.user.is_superuser or self.request.user.is_staff

    def get_success_url(self):
        messages.success(self.request, "Tarea eliminada correctamente.")
        return reverse_lazy('tarea_list', kwargs={'proyecto_id': self.object.proyecto.id})



# Vistas de Mensajes

# Vista para listar mensajes
class MensajeListView(LoginRequiredMixin, ListView):
    model = Mensaje
    template_name = 'mensajes/mensaje_list.html'
    context_object_name = 'mensajes'

    def get_queryset(self):
        proyecto_id = self.kwargs.get('proyecto_id')
        if proyecto_id:
            proyecto = get_object_or_404(Proyecto, id=proyecto_id)
            grupos = proyecto.grupos.all()
            queryset = Mensaje.objects.filter(
                models.Q(grupo__in=grupos) | 
                models.Q(usuario_receptor=self.request.user) | 
                models.Q(usuario_emisor=self.request.user)
            ).order_by('-fecha_envio')
            print(f"Queryset para proyecto {proyecto_id}: {queryset}")
            return queryset
        queryset = Mensaje.objects.filter(
            models.Q(usuario_receptor=self.request.user) | 
            models.Q(usuario_emisor=self.request.user)
        ).order_by('-fecha_envio')
        print(f"Queryset general: {queryset}")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyecto_id'] = self.kwargs.get('proyecto_id')
        return context
    

    
# Vista para crear un mensaje (individual o grupal)
class MensajeCreateView(LoginRequiredMixin, CreateView):
    model = Mensaje
    form_class = MensajeForm
    template_name = 'mensajes/mensaje_form.html'
    success_url = reverse_lazy('mensajes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['proyecto_id'] = self.kwargs.get('proyecto_id')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyecto_id'] = self.kwargs.get('proyecto_id')
        return context

    def get_success_url(self):
        proyecto_id = self.kwargs.get('proyecto_id')
        return reverse_lazy('mensajes_proyecto', kwargs={'proyecto_id': proyecto_id}) if proyecto_id else reverse_lazy('mensajes')

    def form_valid(self, form):
        form.instance.usuario_emisor = self.request.user
        proyecto_id = self.kwargs.get('proyecto_id')
        if proyecto_id:
            proyecto = get_object_or_404(Proyecto, id=proyecto_id)
            if form.cleaned_data['receptor_type'] == 'group' and form.cleaned_data['grupo']:
                form.instance.grupo = form.cleaned_data['grupo']
                form.instance.usuario_receptor = None
            elif form.cleaned_data['receptor_type'] == 'user':
                form.instance.grupo = None
        return super().form_valid(form)   
    
# Vista para responder a un mensaje
class MensajeReplyCreateView(LoginRequiredMixin, CreateView):
    model = Mensaje
    form_class = MensajeForm
    template_name = 'mensajes/mensaje_reply_form.html'
    success_url = reverse_lazy('mensajes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['proyecto_id'] = self.kwargs.get('proyecto_id')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyecto_id'] = self.kwargs.get('proyecto_id')
        mensaje_id = self.kwargs.get('mensaje_id')
        if mensaje_id:
            context['mensaje_original'] = get_object_or_404(Mensaje, id=mensaje_id)
        return context

    def get_success_url(self):
        proyecto_id = self.kwargs.get('proyecto_id')
        return reverse_lazy('mensajes_proyecto', kwargs={'proyecto_id': proyecto_id}) if proyecto_id else reverse_lazy('mensajes')

    def form_valid(self, form):
        form.instance.usuario_emisor = self.request.user
        proyecto_id = self.kwargs.get('proyecto_id')
        mensaje_id = self.kwargs.get('mensaje_id')
        if proyecto_id and mensaje_id:
            proyecto = get_object_or_404(Proyecto, id=proyecto_id)
            mensaje_original = get_object_or_404(Mensaje, id=mensaje_id)
            if mensaje_original.grupo:
                form.instance.grupo = mensaje_original.grupo
                form.instance.usuario_receptor = None
            else:
                form.instance.usuario_receptor = mensaje_original.usuario_emisor
                form.instance.grupo = None
        return super().form_valid(form)
    
    
# Vista para eliminar un mensaje                                  
class MensajeDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        mensaje = get_object_or_404(Mensaje, id=self.kwargs['mensaje_id'])
        if mensaje.usuario_emisor == request.user or request.user.is_superuser:
            mensaje.delete()
        return redirect('mensajes_proyecto', proyecto_id=self.kwargs['proyecto_id'])


#Comentario


class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentarios/comentario_form.html'

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
    template_name = 'notificaciones/notificaciones.html'  # Ajusta según tu estructura
    context_object_name = 'notificaciones'

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Notificacion.objects.filter(leida=False).order_by('-fecha')
        else:
            queryset = Notificacion.objects.filter(
                usuario=self.request.user,
                leida=False
            ).order_by('-fecha')
        print(f"Notificaciones para {self.request.user}: {queryset}")
        return queryset
        



@login_required
def marcar_notificacion_leida(request, notificacion_id):
    if request.method == 'POST':
        try:
            print(f"Intentando marcar notificación {notificacion_id} para el usuario {request.user}")
            notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
            print(f"Notificación encontrada: {notificacion}")
            notificacion.leida = True
            notificacion.save()
            print("Notificación guardada correctamente")
            messages.success(request, "Notificación marcada como leída.")  # Usa 'messages', no 'mensajes'
        except Notificacion.DoesNotExist:
            print(f"Notificación {notificacion_id} no encontrada o no pertenece al usuario {request.user}")
            messages.error(request, "No tienes permiso para marcar esta notificación o no existe.")  # Usa 'messages'
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            messages.error(request, f"Error al marcar la notificación: {str(e)}")  # Usa 'messages'
    return redirect(reverse_lazy('notificaciones'))