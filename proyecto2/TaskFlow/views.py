from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Proyecto
from .forms import RegistroForm, ProyectoForm
from .mixins import AdminRequiredMixin

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
    template_name = 'proyecto_list.html'

class ProyectoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_form.html'
    success_url = '/proyectos/'

class ProyectoUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyecto_update.html'  # Nueva plantilla para edición
    success_url = '/proyectos/'  # Redirige a la lista tras actualizar

    def get_queryset(self):
        # Restringe la edición solo a los proyectos que el usuario puede modificar
        return Proyecto.objects.all()  # Ajusta esto si quieres más restricciones (por ejemplo, solo proyectos del usuario)