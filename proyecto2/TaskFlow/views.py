from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegistroForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from .models import Proyecto

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

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol == 'admin'

class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyecto_list.html'

class ProyectoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Proyecto
    fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'usuarios']
    template_name = 'proyecto_form.html'