from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Proyecto
from .models import Tarea
from .models import Comentario
from .models import Mensaje

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
        fields = ['nombre', 'descripcion', 'fecha_limite', 'estado', 'usuarios_asignados', 'asignado_a']
                        
# Formulario para crear comentarios
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']

# Formulario para enviar mensajes
class MensajeForm(forms.ModelForm):
    destinatario = forms.ModelChoiceField(queryset=User.objects.all(), label="Destinatario")

    class Meta:
        model = Mensaje
        fields = ['destinatario', 'contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4}),
        }