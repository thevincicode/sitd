# Create your views here.
from sitdapp.models import Expediente, Oficina,Trabajador, ExpedienteHistorial
from django.db import connection, transaction
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse



def expedientes(request):
	expedientes= Expediente.objects.filter(estado=1)
	#expedientes=get_object_or_404(Expediente, estado=1)
	return render_to_response('expedietes.html',{'lista':expedientes})

def expediente_detalle(request,id_expediente):
	expediente=get_object_or_404(Expediente, pk=id_expediente)
	historial=ExpedienteHistorial.objects.filter(expediente=expediente)
	return render_to_response('expediente_detalle.html',{'expediente':expediente, 'historial':historial},context_instance=RequestContext(request))

"""def list_exp(request):
    cursor = connection.cursor()
    cursor.execute('SELECT `sitdapp_expediente`.*, `sitdapp_oficina`.`nombre` FROM `dbsitd`.`sitdapp_expediente` INNER JOIN `dbsitd`.`sitdapp_oficina` ON (`sitdapp_expediente`.`oficina_id` = `sitdapp_oficina`.`id`)',[self.baz]) 
	row =  cursor.fetchall()

    return render_to_response('lista_expedietes.html',{'lista':row})

    """

def login(request):
	 # If we submitted the form...
    if request.method == 'POST':

        # Check that the test cookie worked (we set it below):
        if request.session.test_cookie_worked():

            # The test cookie worked, so delete it.
            request.session.delete_test_cookie()

            # In practice, we'd need some logic to check username/password
            # here, but since this is an example...
            return HttpResponse("You're logged in.")

        # The test cookie failed, so display an error message. If this
        # was a real site we'd want to display a friendlier message.
        else:
            return HttpResponse("Please enable cookies and try again.")

    # If we didn't post, send the test cookie along with the login form.
    request.session.set_test_cookie()
    return render_to_response('foo/login_form.html')
    #aca devemos agregar un codigo para logear
    try:
        m = Trabajador.objects.get(username__exact=request.POST['usuario'])
        if m.password == request.POST['pwd']:
            request.session['member_id'] = m.id
            return HttpResponse("You're logged in.")
    except Trabajador.DoesNotExist:
        return HttpResponse("Your username and password didn't match.")

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

