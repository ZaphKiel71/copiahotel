from django import forms
from .models import Nacionalidad, TipoUsuario, Usuario, Habitacion, Pago, Pasajero

class NacionalidadForm(forms.ModelForm):
    class Meta:
        model = Nacionalidad
        fields = ['codigo_naci', 'descripcion']  # Cambia 'Descripcion' a 'descripcion'
        widgets = {
            'codigo_naci': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),  # Cambia 'Descripcion' a 'descripcion'
        }

class TipoUsuarioForm(forms.ModelForm):
    class Meta:
        model = TipoUsuario
        fields = ['descripcion']  # Especifica los campos que quieres mostrar en el formulario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'password'] 

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['tipo_habitacion', 'estado_habitacion']

    def __init__(self, *args, **kwargs):
        super(HabitacionForm, self).__init__(*args, **kwargs)
        self.fields['tipo_habitacion'].widget.attrs.update({'class': 'form-control'})

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['id_pasajero', 'fecha', 'pago_total', 'metodo_pago']

class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = [ 'rut', 'nombre', 'apellido_paterno', 'apellido_materno', 'correo', 'codigo_naci']  # Ajusta según tus campos