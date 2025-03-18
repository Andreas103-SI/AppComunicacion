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
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 3}),
        }
        
        
# Formulario para enviar mensajes

class MensajeForm(forms.ModelForm):
    receptor_type = forms.ChoiceField(
        choices=[
            ('user', 'Usuario individual'),
            ('group', 'Grupo'),
        ],
        widget=forms.RadioSelect,
        initial='user'
    )
    usuario_receptor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Destinatario (si es usuario)"
    )
    grupo = forms.ModelChoiceField(
        queryset=Grupo.objects.none(),  # Se poblará dinámicamente
        required=False,
        label="Grupo (si es grupo)"
    )

    class Meta:
        model = Mensaje
        fields = ['receptor_type', 'usuario_receptor', 'grupo', 'contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        proyecto_id = kwargs.pop('proyecto_id', None)
        super().__init__(*args, **kwargs)
        # Solo filtra usuario_receptor si hay una instancia y un usuario_emisor válido
        if 'instance' in kwargs and kwargs['instance'] and hasattr(kwargs['instance'], 'usuario_emisor'):
            self.fields['usuario_receptor'].queryset = User.objects.exclude(id=kwargs['instance'].usuario_emisor.id)
        if proyecto_id:
            self.fields['grupo'].queryset = Grupo.objects.filter(proyecto_id=proyecto_id)
        if self.data.get('receptor_type') == 'user':
            self.fields['usuario_receptor'].required = True
            self.fields['grupo'].required = False
        elif self.data.get('receptor_type') == 'group':
            self.fields['grupo'].required = True
            self.fields['usuario_receptor'].required = False

    def clean(self):
        cleaned_data = super().clean()
        receptor_type = cleaned_data.get('receptor_type')
        if receptor_type == 'user' and not cleaned_data.get('usuario_receptor'):
            raise forms.ValidationError("Debes seleccionar un destinatario si eliges 'Usuario individual'.")
        elif receptor_type == 'group' and not cleaned_data.get('grupo'):
            raise forms.ValidationError("Debes seleccionar un grupo si eliges 'Grupo'.")
        return cleaned_data