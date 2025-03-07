from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Proyecto
from .models import Tarea

User = get_user_model()

# Formulario para registrar nuevos usuarios
class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'rol']  # Ajusta según los campos de tu modelo Usuario

# Formulario para crear proyectos
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'usuarios']
        widgets = {
            'usuarios': forms.SelectMultiple(),
        }
# Formulario para crear tareas
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'fecha_limite', 'fecha_vencimiento', 'estado', 'usuarios_asignados', 'asignado_a']
        widgets = {
            'usuarios_asignados': forms.SelectMultiple(),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }