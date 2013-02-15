# Create your views here.
from sitdapp.models import Expediente
from django.shortcuts import render_to_response

def lista_expedientes(request):
	expedientes= Expediente.objects.all()
	return render_to_response('lista_expedietes.html',{'lista':expedientes})