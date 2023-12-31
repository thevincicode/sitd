# encoding:utf-8
from django.forms import ModelForm
from django import forms
from sitdapp.models import Tupa, TupaRequisitos, Proveido, ExpedienteTipo, Organizacion, Trabajador, Oficina


class TupaForm(ModelForm):
    class Meta:
        model = Tupa
        fields = ['denominacion', 'descripcion',
                  'autoridad', 'porcentaje', 'valor', 'tiempo']


class TupaRequisitosForm(ModelForm):
    class Meta:
        model = TupaRequisitos
        fields = ['requisito', 'descripcion']


class ProveidoForm(ModelForm):
    class Meta:
        model = Proveido
        fields = ['nombre', 'descripcion']


class ExpedienteTipoForm(ModelForm):
    class Meta:
        model = ExpedienteTipo
        fields = ['nombre', 'descripcion']


class OrganizacionForm(ModelForm):
    class Meta:
        model = Organizacion
        fields = ['nombre', 'logo', 'direccion']
# sergio


class LogueoNuevoForm(forms.Form):
    Usuario = forms.CharField(widget=forms.TextInput())
    Contrasena = forms.CharField(widget=forms.PasswordInput())


class OficinaNuevoForm(forms.Form):
    Nombre = forms.CharField(widget=forms.TextInput())
    Descripcion = forms.CharField(widget=forms.Textarea(), required=False)


class TrabajadorNuevoForm(ModelForm):
    class Meta:
        model = Trabajador
        fields = ['dni', 'nombre', 'apellidos', 'f_nacimiento',
                  'cargo', 'usuario', 'psw', 'oficina', 'admin']


class OficinaForm(ModelForm):
    class Meta:
        model = Oficina
        fields = ['nombre', 'descripcion']
