from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Proyecto
from .models import Tarea
from .models import Comentario
from .models import Mensaje, Grupo

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
    usuario_receptor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Destinatario",
        required=False  # Permitir que sea opcional si se selecciona un grupo
    )
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.all(),
        label="Grupo",
        required=False  # Permitir que sea opcional si se selecciona un usuario
    )

    class Meta:
        model = Mensaje
        fields = ['usuario_receptor', 'grupo', 'contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        usuario_receptor = cleaned_data.get('usuario_receptor')
        grupo = cleaned_data.get('grupo')

        # Validar que se seleccione un usuario o un grupo, pero no ambos
        if not usuario_receptor and not grupo:
            raise forms.ValidationError("Debes seleccionar un usuario o un grupo como destinatario.")
        if usuario_receptor and grupo:
            raise forms.ValidationError("No puedes seleccionar un usuario y un grupo al mismo tiempo.")
        return cleaned_data