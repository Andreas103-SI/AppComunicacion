from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView #Agrega DetailView a la lista de importaciones.
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
        print(f"Usuario autenticado: {self.request.user}, Autenticado: {self.request.user.is_authenticated}")  # Depuración
        if proyecto_id:
            if self.request.user.is_superuser or self.request.user.is_staff:
                print("Usuario es superusuario o staff, mostrando todas las tareas.")
                tareas = Tarea.objects.filter(proyecto_id=proyecto_id)
            elif self.request.user.is_authenticated:
                print(f"Filtrando tareas para usuario ID: {self.request.user.id}")  # Depuración
                q1 = models.Q(asignado_a=self.request.user)
                q2 = models.Q(usuarios_asignados=self.request.user)
                try:
                    print("Q1 creado:", q1)  # Depuración
                    print("Q2 creado:", q2)  # Depuración
                    tareas = Tarea.objects.filter(proyecto_id=proyecto_id).filter(q1 | q2)
                except Exception as e:
                    print(f"Error al crear el filtro: {e}")
                    tareas = Tarea.objects.none()
            else:
                print("Usuario no autenticado, devolviendo queryset vacío.")
                tareas = Tarea.objects.none()
            print(f"Tareas encontradas: {list(tareas)}")  # Depuración
            return tareas
        print("Proyecto ID no proporcionado, devolviendo queryset vacío.")
        return Tarea.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proyecto_id = self.kwargs.get('proyecto_id')
        context['proyecto_id'] = proyecto_id
        if proyecto_id:
            try:
                context['proyecto'] = get_object_or_404(Proyecto, id=proyecto_id)
            except Proyecto.DoesNotExist:
                context['proyecto'] = None
        else:
            context['proyecto'] = None
        return context
    

class TareaCreateView(LoginRequiredMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/tarea_form.html'

    def form_valid(self, form):
        proyecto_id = self.kwargs.get('proyecto_id')
        print(f"Proyecto ID desde URL: {proyecto_id}")  # Depuración
        if not proyecto_id:
            raise ValueError("No se proporcionó un proyecto_id en la URL.")
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        print(f"Proyecto encontrado: {proyecto}")  # Depuración
        form.instance.proyecto = proyecto
        print(f"Proyecto asignado a la tarea: {form.instance.proyecto}")  # Depuración
        
        # Guardar la tarea
        response = super().form_valid(form)
        
        # Generar notificaciones para los usuarios asignados
        tarea = self.object  # La tarea recién creada
        if tarea.asignado_a:
            Notificacion.objects.create(
                usuario=tarea.asignado_a,
                mensaje=f"Se te ha asignado la tarea '{tarea.nombre}' en el proyecto '{proyecto.nombre}'."
            )
        for usuario in tarea.usuarios_asignados.all():
            Notificacion.objects.create(
                usuario=usuario,
                mensaje=f"Has sido asignado a la tarea '{tarea.nombre}' en el proyecto '{proyecto.nombre}'."
            )
        
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
        # Muestra mensajes enviados o recibidos por el usuario, o mensajes dirigidos a un grupo al que pertenece
        return Mensaje.objects.filter(
            models.Q(usuario_receptor=self.request.user) |
            models.Q(usuario_emisor=self.request.user) |
            models.Q(grupo__usuarios=self.request.user)
        ).order_by('-fecha_envio')

class MensajeCreateView(LoginRequiredMixin, CreateView):
    model = Mensaje
    form_class = MensajeForm
    template_name = 'mensajes/mensaje_form.html'
    success_url = reverse_lazy('mensajes')

    def form_valid(self, form):
        form.instance.usuario_emisor = self.request.user
        return super().form_valid(form)
        
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