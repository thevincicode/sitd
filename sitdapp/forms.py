from django.forms import ModelForm
from django import forms
from sitdapp.models import Tupa, TupaRequisitos, Proveido, ExpedienteTipo, Organizacion, Trabajador, Oficina

class TupaForm(ModelForm):
	class Meta:
		model=Tupa

class TupaRequisitosForm(ModelForm):
	class Meta:
		model=TupaRequisitos

class ProveidoForm(ModelForm):
	class Meta:
		model=Proveido

class ExpedienteTipoForm(ModelForm):
	class Meta:
		model=ExpedienteTipo

class OrganizacionForm(ModelForm):
	class Meta:
		model=Organizacion
#sergio
class LogueoNuevoForm(forms.Form):
	Usuario	= forms.CharField(widget=forms.TextInput())
	Contrasena=forms.CharField(widget=forms.PasswordInput())

class OficinaNuevoForm(forms.Form):
	Nombre	=forms.CharField(widget=forms.TextInput())
	Descripcion	=forms.CharField(widget=forms.Textarea(),required=False)

class TrabajadorNuevoForm(ModelForm):
	class Meta:
		model=Trabajador

class OficinaForm(ModelForm):
	class Meta:
		model=Oficina
