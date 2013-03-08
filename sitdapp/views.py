# Create your views here.
from sitdapp.models import Expediente, ExpedienteTipo, Oficina,Trabajador, ExpedienteHistorial, Derivar, DerivarDetalle ,Proveido, Organizacion, Tupa, TupaRequisitos, TupaVinculo
from sitdapp.forms import TupaForm, TupaRequisitosForm, ExpedienteTipoForm, ProveidoForm, OrganizacionForm,LogueoNuevoForm,OficinaNuevoForm,TrabajadorNuevoForm
from django.db import connection, transaction
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

#ahora = str(datetime.now()) 


def expedientes(request):
    try: 
        empresa = Organizacion.objects.get(id=1)
        ahora = datetime.now().strftime("%d-%m-%Y")
        #ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
        #today = datetime.now()
        oficinas = Oficina.objects.all()
        proveidos = Proveido.objects.all()
        expediente = Expediente.objects.filter(estado="R")
        #expedientes=get_object_or_404(Expediente, estado=1)
        return render_to_response('expedientes.html',{'lista':expediente,'oficinas':oficinas,'proveidos':proveidos,'fecha':ahora, 'organizacion':empresa},context_instance=RequestContext(request))
    except Organizacion.DoesNotExist:
      # we have no object!  do something
      pass
    

def archivados(request):
    #ahora = datetime.datetime.now()
    oficinas = Oficina.objects.all()
    proveidos = Proveido.objects.all()
    expediente = Expediente.objects.filter(estado="A")
    #expedientes=get_object_or_404(Expediente, estado=1)
    return render_to_response('archivados.html',{'lista':expediente,'oficinas':oficinas,'proveidos':proveidos},context_instance=RequestContext(request))

def porrecibir(request):
    #ahora = datetime.datetime.now()
    oficinas = Oficina.objects.all()
    proveidos = Proveido.objects.all()
    expediente = Expediente.objects.filter(estado="E")
    #expedientes=get_object_or_404(Expediente, estado=1)
    return render_to_response('porrecibir.html',{'lista':expediente,'oficinas':oficinas,'proveidos':proveidos},context_instance=RequestContext(request))

def expediente_detalle(request,id_expediente):
	expediente=get_object_or_404(Expediente, pk=id_expediente)
	historial=ExpedienteHistorial.objects.filter(expediente=expediente)
	return render_to_response('expediente_detalle.html',{'expediente':expediente, 'historial':historial},context_instance=RequestContext(request))

def expediente_detalle_comentario(request,id_expediente,id_historial):
    expediente=get_object_or_404(Expediente, pk=id_expediente)
    #historial=ExpedienteHistorial.objects.filter(expediente=expediente)
    historial=get_object_or_404(ExpedienteHistorial, pk=id_historial)
    return render_to_response('comentario.html',{'expediente':expediente, 'historial':historial},context_instance=RequestContext(request))

def buscador(request):    
    if request.GET.get("b"):
        buscar = str(''+ request.GET["b"]+'')
        try:
            buscar=int(buscar)
            buscador=Expediente.objects.filter(nro_exp=buscar)
            return render_to_response('buscador.html',{'lista':buscador},context_instance=RequestContext(request))    
        except Exception, e:
            buscador=Expediente.objects.filter(interesado__contains=buscar)
            return render_to_response('buscador.html',{'lista':buscador},context_instance=RequestContext(request))    
            print "parametro a buscar es: " + buscar
            #buscar = '%r' % request.GET['b']
        
    else:
        html="<html><body>no envio ningun parametro</body></html>"
        return HttpResponse(html)
    

def expediente_derivar(request):
    if request.method == "POST":
        id_s = request.POST.getlist("hi")
        comentario = request.POST.get('comentarioA','')
        oficina_s = request.POST.getlist("oficina")
        proveido_s = request.POST.getlist("proveido")
        print 'documentos ' + str(len(id_s))
        print 'oficinas ' + str(len(oficina_s))
        print 'proveidos ' + str(len(proveido_s))
        print 'el comentario fue: ' + comentario
        #html="<html><body>logramos capturar datos, intentando acceder</body></html>"
        try:
            if(len(id_s)>0): 
                print "entro, hay documentos"       
                for v in id_s:
                    indexx=id_s.index(str(v))
                    idexp=id_s[indexx]
                    print "primer for de documentos id= " + idexp
                    print "el indice es " + str(indexx)
                    ahora = str(datetime.now())
                    #obteniendo el id del select proveido
                    for o in oficina_s:
                        print "segundo for de oficinas " + o
                        #for p in proveido_s:
                            #print "tercer for de proveidos " + p
                            #if(proveido_s[indexx]==idpro):
                        print 'el id de select proveido es '+proveido_s[indexx]
                        idproveido=proveido_s[indexx]
                        print 'el id proveido es ' + str(idproveido)
                        proveido = get_object_or_404(Proveido, pk=idproveido)
                        idoficina=o
                        oficina = get_object_or_404(Oficina, pk=idoficina)
                        #generando un objeto de tipo Derivar y guardando
                        derivar_obj=Derivar(fecha=datetime.now(),estado="E",comentario=comentario,proveido=proveido,oficina=oficina)
                        derivar_obj.save()
                        print "se derivo"
                        #obteniendo el ultimo id registrado
                        id_derivar_obj=derivar_obj.id
                        #generando un objeto de tipo DerivarDetalle y guardando
                        idexpediente=v
                        expediente=get_object_or_404(Expediente, pk=idexpediente)
                        derivar=get_object_or_404(Derivar, pk=id_derivar_obj)
                        derivardetalle_obj=DerivarDetalle(fecha=datetime.now(), expediente=expediente, derivar=derivar)
                        derivardetalle_obj.save()
                        print "se derivo completo "
                        oficina_o=expediente.oficina
                        #agregando al historial
                        historial_obj=ExpedienteHistorial(f_salida=datetime.now(),o_origen=oficina_o,o_destino=oficina.nombre,f_recepcion=datetime.now(),estado="enviado", proveido=proveido.nombre,expediente=expediente, ubicacion="-",comentario=comentario)
                        historial_obj.save()
                        print "se agrego al historial"
                        #actualizando estado del expediente
                        expediente_upd=Expediente.objects.get(pk=idexpediente)
                        expediente_upd.oficina=oficina
                        expediente_upd.save()
                        #expediente_upd.estado="E"
                        print "se actualizo la oficina del expediente"
                        #expediente_upd.save()
                        html="<html><body>los datos fueron registrados</body></html>"
                return HttpResponse(html)
            else:
                html="<html><body>llego vacio</body></html>"
                return HttpResponse(html)
        except Exception, e:  
            html="<html><body>error accediendo<br>"+str(e)+"</body></html>"  
            return HttpResponse(html)
    else:
        html="<html><body>Error de envio</body></html>"
        return HttpResponse(html)
        
def expediente_archivar(request):
    if request.method == "POST":
        id_s = request.POST.getlist("hi")
        comentario = request.POST.get('comentarioA','')
        #oficina = request.POST.get('oficina', '')
        print 'documentos ' + str(len(id_s))
        #html="<html><body>logramos capturar datos, intentando acceder</body></html>"
        try:
            if(len(id_s)>0): 
                print "entro, hay documentos"       
                for v in id_s:
                    indexx=id_s.index(str(v))
                    idexp=id_s[indexx]
                    print "primer for de documentos id= " + idexp
                    print "el indice es " + str(indexx)
                    #obteniendo el id del select proveido
                    idexpediente=v
                    #actualizando estado del expediente
                    expediente_upd=Expediente.objects.get(pk=idexpediente)
                    expediente_upd.estado="A"
                    expediente_upd.archivomotivo=comentario
                    expediente_upd.save()
                    #expediente_upd.estado="E"
                    print "se Archivo la oficina del expediente"
                    #expediente_upd.save()
                    html="<html><body>los documentos fueron Archivados</body></html>"
                return HttpResponse(html)
            else:
                html="<html><body>llego vacio</body></html>"
                return HttpResponse(html)
        except Exception, e:  
            html="<html><body>error accediendo<br>"+str(e)+"</body></html>"  
            return HttpResponse(html)
    else:
        html="<html><body>Error de envio</body></html>"
        return HttpResponse(html)

def expediente_recibir(request):
    if request.method == "POST":
        id_s = request.POST.getlist("hi")
        #oficina = request.POST.get('oficina', '')
        print 'documentos ' + str(len(id_s))
        #html="<html><body>logramos capturar datos, intentando acceder</body></html>"
        try:
            if(len(id_s)>0): 
                print "entro, hay documentos"       
                for v in id_s:
                    indexx=id_s.index(str(v))
                    idexp=id_s[indexx]
                    print "primer for de documentos id= " + idexp
                    print "el indice es " + str(indexx)
                    #obteniendo el id del select proveido
                    idexpediente=v
                    #actualizando estado del expediente
                    expediente_upd=Expediente.objects.get(pk=idexpediente)
                    expediente_upd.estado="R"
                    expediente_upd.save()
                    #expediente_upd.estado="E"
                    print "se Archivo la oficina del expediente"
                    #expediente_upd.save()
                    html="<html><body>los documentos fueron recibidos</body></html>"
                return HttpResponse(html)
            else:
                html="<html><body>llego vacio</body></html>"
                return HttpResponse(html)
        except Exception, e:  
            html="<html><body>error accediendo<br>"+str(e)+"</body></html>"  
            return HttpResponse(html)
    else:
        html="<html><body>Error de envio</body></html>"
        return HttpResponse(html)

# el famoso tupa
def tupa_lista(request):
    tupa=Tupa.objects.all()
    return render_to_response('tupa_lista.html',{'lista':tupa},context_instance=RequestContext(request))

def tupa_nuevo(request):
    if request.method=='POST':
        formulario=TupaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/tupa')
    else:
        formulario=TupaForm()
    return render_to_response('tupaform.html',{'formulario':formulario},context_instance=RequestContext(request))

def tupa_editar(request, id_tupa):    
    tupa=get_object_or_404(Tupa,pk=id_tupa)
    formulario=TupaForm(request.POST or None, instance=tupa)
    if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect('/tupa')
    return render_to_response('tupaform.html',{'formulario':formulario},context_instance=RequestContext(request))
   
def tupa_eliminar(request,id_tupa):
    try:
        tupa=Tupa.objects.get(pk=id_tupa)
        tupa.delete()
        return HttpResponse('delete')
    except Exception, e:
        raise e
        return HttpResponseRedirect('/tupa')

#requisitos del tupa
def tuparequisitos_lista(request):
    tupa=TupaRequisitos.objects.all()
    return render_to_response('tuparequisitos_lista.html',{'lista':tupa},context_instance=RequestContext(request))

def tuparequisitos_nuevo(request):
    if request.method=='POST':
        formulario=TupaRequisitosForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/tupa/requisitos')
    else:
        formulario=TupaRequisitosForm()
    return render_to_response('tuparequisitosform.html',{'formulario':formulario},context_instance=RequestContext(request))

def tuparequisitos_editar(request, id_requisito):    
    tupa=get_object_or_404(TupaRequisitos,pk=id_requisito)
    formulario=TupaRequisitosForm(request.POST or None, instance=tupa)
    if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect('/tupa/requisitos')
    return render_to_response('tuparequisitosform.html',{'formulario':formulario},context_instance=RequestContext(request))
   
def tuparequisitos_eliminar(request,id_requisito):
    try:
        tupa=TupaRequisitos.objects.get(pk=id_requisito)
        tupa.delete()
        return HttpResponse('delete')
    except Exception, e:
        raise e
        return HttpResponseRedirect('/tupa/requisitos')

#vincular el tupa con sus requisitos
def tupavincular(request):
    if request.method == "POST":
        id_v = request.POST.getlist("hi")
        id_r = request.POST.get("che")
        #oficina = request.POST.get('oficina', '')
        print 'documentos ' + str(len(id_r))
        #html="<html><body>logramos capturar datos, intentando acceder</body></html>"
        try:
            if(len(id_r)>0): 
                print "entro, hay documentos"       
                tupa=get_object_or_404(Tupa,pk=id_r)
                for v in id_r:
                    id_requisito=v
                    requisitos=get_object_or_404(TupaRequisitos, pk=id_requisito)
                    #actualizando estado del expediente
                    vincular_obj=TupaVinculo(tupa=tupa,requisitos=requisitos)
                    vincular_obj.save()
                    #expediente_upd.estado="E"
                    print "se vinculo correctamente"
                    #expediente_upd.save()
                    html="<html><body>los requisitos fueron vinculados</body></html>"
                return HttpResponse(html)
            else:
                html="<html><body>llego vacio</body></html>"
                return HttpResponse(html)
        except Exception, e:  
            html="<html><body>error accediendo<br>"+str(e)+"</body></html>"  
            return HttpResponse(html)
    else:
        html="<html><body>Error de envio</body></html>"
        return HttpResponse(html)

def tupavinculo_nuevo(request, id_tupa):
    tupa=get_object_or_404(Tupa,pk=id_tupa)
    requisitos=TupaRequisitos.objects.all()
    return render_to_response('tupavinculo.html',{'tupa':tupa,'requisitos':requisitos},context_instance=RequestContext(request))

def tupavinculo_listar(request, id_tupa):
    tupas=get_object_or_404(Tupa,pk=id_tupa)
    vinculo=TupaVinculo.objects.filter(tupa=tupas)
    #requisitos=TupaRequisitos.objects.filter(id=vinculo.requisitos)
    return render_to_response('tupavinculo_detalle.html',{'tupas':tupas,'requisitos':vinculo},context_instance=RequestContext(request))

def tupavinculo_editarguardar(request):    
    if request.method == "POST":
        id_t = request.POST.get("hi")
        id_r = request.POST.getlist("che")
        #oficina = request.POST.get('oficina', '')
        print 'requisitos ' + str(len(id_r))
        #html="<html><body>logramos capturar datos, intentando acceder</body></html>"
        tupa=get_object_or_404(Tupa,pk=id_t)
        vinculo=TupaVinculo.objects.filter(tupa=tupa)
        vinculo.delete()
        try:
            if(len(id_r)>0): 
                print "entro, hay documentos"       
                for v in id_r:
                    id_requisito=v
                    requisitos=get_object_or_404(TupaRequisitos, pk=id_requisito)
                    #actualizando estado del expediente
                    vincular_obj=TupaVinculo(tupa=tupa,requisitos=requisitos)
                    vincular_obj.save()
                    #expediente_upd.estado="E"
                    print "se vinculo correctamente"
                    #expediente_upd.save()
                    html="<html><body>los requisitos fueron vinculados</body></html>"
                return HttpResponse(html)
            else:
                html="<html><body>llego vacio</body></html>"
                return HttpResponse(html)
        except Exception, e:  
            html="<html><body>error accediendo<br>"+str(e)+"</body></html>"  
            return HttpResponse(html)
    else:
        html="<html><body>Error de envio</body></html>"
        return HttpResponse(html)

def tupavinculo_editar(request, id_tupa):
    tupa=get_object_or_404(Tupa,pk=id_tupa)
    requisitos=TupaRequisitos.objects.all()
    return render_to_response('tupavinculo_editar.html',{'tupa':tupa,'requisitos':requisitos},context_instance=RequestContext(request))

def tupavinculo_eliminar(request,id_tupa):
    try:
        tupas=get_object_or_404(Tupa,pk=id_tupa)
        vinculo=TupaVinculo.objects.filter(tupa=tupas)
        vinculo.delete()
        return HttpResponse('delete')
    except Exception, e:
        raise e
        return HttpResponseRedirect('/tupa/requisitos')

# proveidos
def proveido_lista(request):
    tupa=Proveido.objects.all()
    return render_to_response('proveido_lista.html',{'lista':tupa},context_instance=RequestContext(request))

def proveido_nuevo(request):
    if request.method=='POST':
        formulario=ProveidoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/proveidos')
    else:
        formulario=ProveidoForm()
    return render_to_response('proveidoform.html',{'formulario':formulario},context_instance=RequestContext(request))

def proveido_editar(request, id_proveido):    
    tupa=get_object_or_404(Proveido,pk=id_proveido)
    formulario=ProveidoForm(request.POST or None, instance=tupa)
    if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect('/proveidos')
    return render_to_response('proveidoform.html',{'formulario':formulario},context_instance=RequestContext(request))
   
def proveido_eliminar(request,id_proveido):
    try:
        proveido=Proveido.objects.get(pk=id_proveido)
        proveido.delete()
        return HttpResponse('delete')
    except Exception, e:
        raise e
        return HttpResponseRedirect('/proveidos')

# tipos de expedientes
def expedientetipo_lista(request):
    tupa=ExpedienteTipo.objects.all()
    return render_to_response('expedientetipo_lista.html',{'lista':tupa},context_instance=RequestContext(request))

def expedientetipo_nuevo(request):
    if request.method=='POST':
        formulario=ExpedienteTipoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/expediente/tipos')
    else:
        formulario=ExpedienteTipoForm()
    return render_to_response('expedientetipoform.html',{'formulario':formulario},context_instance=RequestContext(request))

def expedientetipo_editar(request, id_tipo):    
    tupa=get_object_or_404(Proveido,pk=id_tipo)
    formulario=ExpedienteTipoForm(request.POST or None, instance=tupa)
    if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect('/expediente/tipos')
    return render_to_response('expedientetipoform.html',{'formulario':formulario},context_instance=RequestContext(request))
   
def expedientetipo_eliminar(request,id_tipo):
    try:
        exptipo=ExpedienteTipo.objects.get(pk=id_tipo)
        exptipo.delete()
        return HttpResponse('delete')
    except Exception, e:
        raise e
        return HttpResponseRedirect('/expediente/tipos')

def organizacion_listar(request):
    organizacion=Organizacion.objects.all()
    return render_to_response('organizacion_lista.html',{'lista':organizacion},context_instance=RequestContext(request))

def organizacion_editar(request, id_org):
    organizacion=get_object_or_404(Organizacion,pk=id_org)
    formulario=OrganizacionForm(request.POST or None,instance=organizacion) 
    if formulario.is_valid():
        formulario.save()
        return HttpResponseRedirect('/organizacion')
    return render_to_response('organizacionform.html',{'formulario':formulario},context_instance=RequestContext(request))

#sergio
def TrabajadorControl(request):
    Lista=Trabajador.objects.all()
    Ctx={'Form':Lista}
    return render_to_response('TrabajadorControl.html',Ctx,context_instance=RequestContext(request))

def TrabajadorNuevo(request):
    if request.method=='POST':
        Info='Inicializando'
        Formulario=TrabajadorNuevoForm(request.POST)
        if Formulario.is_valid():
            try:
                Formulario.save()
                Info='Se registro Nuevo Trabajador'
                Lista=Trabajador.objects.all()
                Ctx={'Info':Info,'Form':Lista}
                return render_to_response('TrabajadorControl.html',Ctx,context_instance=RequestContext(request))
            except:
                Info='Error, El Dni Ingresado Ya Existe'
                Ctx={'Info':Info,'Form':Formulario}
                return render_to_response('TrabajadorNuevo.html',Ctx,context_instance=RequestContext(request))
        else:
            Info='Ingrese toda la informacion solicitada'
            Ctx={'Info':Info,'Form':Formulario}
            return render_to_response('TrabajadorNuevo.html',Ctx,context_instance=RequestContext(request))
    else:
        Info='Error nocrea'
        Formulario=TrabajadorNuevoForm()
        Ctx={'Form':Formulario,'Info':Info}
        return render_to_response('TrabajadorNuevo.html',Ctx,context_instance=RequestContext(request))

def TrabajadorEliminarDesicion(request,id_trabajador):
    EliminarTrabajador=Trabajador.objects.get(pk=id_trabajador)
    Ctx={'id_trabajador':id_trabajador,'Trabajador':EliminarTrabajador}
    return render_to_response('TrabajadorEliminar.html',Ctx,context_instance=RequestContext(request))

def TrabajadorEliminar(request,id_trabajador):
    try:
        '''ALguna Restriccion'''
        EliminarTrabajador=Trabajador.objects.get(pk=id_trabajador)
        EliminarTrabajador.delete()
        Info='Se Elimino el trabajador: '+EliminarTrabajador.nombre+' '+EliminarTrabajador.apellidos
        Lista=Trabajador.objects.all()
        Ctx={'Info':Info,'Form':Lista}
        return render_to_response('TrabajadorControl.html',Ctx,context_instance=RequestContext(request))
    except ObjectDoesNotExist:
        EliminarTrabajador=Trabajador.objects.get(pk=id_trabajador)
        EliminarTrabajador.delete()
        Info='Se Elimino el trabajador: '+EliminarTrabajador.nombre+' '+EliminarTrabajador.apellidos
        Lista=Trabajador.objects.all()
        ctx={'Info':Info,'Form':Lista}
        return render_to_response('TrabajadorControl.html',Ctx,context_instance=RequestContext(request))

def OficinaEliminarDesicion(request,id_oficina):
    EliminarOficina=Oficina.objects.get(pk=id_oficina)
    Ctx={'id_oficina':id_oficina,'Oficina':EliminarOficina}
    return render_to_response('OficinaEliminar.html',Ctx,context_instance=RequestContext(request))

def OficinaEliminar(request,id_oficina):
    try:
        EliminarTrabajador=Trabajador.objects.get(oficina_id=id_oficina)
        Info='Error, No se puede eliminar la oficina La oficina ya esta asignado a un trabajador'
        Lista=Oficina.objects.all()
        Ctx={'Form':Lista,'Info':Info}
        return render_to_response('OficinaControl.html',Ctx,context_instance=RequestContext(request))
        
    except ObjectDoesNotExist:
        EliminarOficina=Oficina.objects.get(pk=id_oficina)
        EliminarOficina.delete()
        Info='Se Elimino la oficina de '+EliminarOficina.nombre
        Lista=Oficina.objects.all()
        Ctx={'Form':Lista,'Info':Info}
        return render_to_response('OficinaControl.html',Ctx,context_instance=RequestContext(request))

def OficinaControl(request):
    Lista=Oficina.objects.all()
    Ctx={'Form':Lista}
    return render_to_response('OficinaControl.html',Ctx,context_instance=RequestContext(request)) 

def OficinaNuevo(request):
    if request.method=='POST':
        Info='Inicializando'
        Formulario=OficinaNuevoForm(request.POST)
        if Formulario.is_valid():
            try:
                Nombre=request.POST['Nombre']
                Descripcion=request.POST['Descripcion']
                O=Oficina()
                O.nombre=Nombre
                O.descripcion=Descripcion
                O.save()
                Info='Se Agrego Nueva Oficina'
                Lista=Oficina.objects.all()
                Ctx={'Form':Lista,'Info':Info}
                return render_to_response('OficinaControl.html',Ctx,context_instance=RequestContext(request))
            except:
                Info='Error, El Nombre Ingresado Ya Existe'
                Ctx={'Info':Info,'Form':Formulario}
                return render_to_response('OficinaNuevo.html',Ctx,context_instance=RequestContext(request))
 
        else:
            Info='Ingrese Toda la Infomacion Solicitada'
            Ctx={'Info':Info,'Form':Formulario}
            return render_to_response('OficinaNuevo.html',Ctx,context_instance=RequestContext(request))
    else:
        Formulario=OficinaNuevoForm()
        Ctx={'Form':Formulario}
        return render_to_response('OficinaNuevo.html',Ctx,context_instance=RequestContext(request))

def LogueoSalir(request):
    if request.method=='POST':
        request.session['EstadoLogueo']=False
        del request.session['IdUsuario']

    Formulario=LogueoNuevoForm()
    request.session['EstadoLogueo']=False
    Info='Info Salida'
    Ctx={'Info':Info,'Form':Formulario}
    return render_to_response('Logueo.html',Ctx,context_instance=RequestContext(request))

def LogueoNuevo(request):
    try:
        EstadoLogueo=False
        if request.session.get('EstadoLogueo',True):
            EstadoLogueo=True
            UsuarioLogueado=Trabajador.objects.get(id=request.session['IdUsuario'])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre
            oficinas = Oficina.objects.all()
            proveidos = Proveido.objects.all()
            expediente = Expediente.objects.filter(estado="R")
            return render_to_response('expedientes.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'EstadoLogueo':EstadoLogueo,'lista':expediente,'oficinas':oficinas,'proveidos':proveidos},context_instance=RequestContext(request))      
        else:
            if request.method=='POST':
                Info='Inicializando'
                Formulario=LogueoNuevoForm(request.POST)
                if Formulario.is_valid():
                    try:
                        UsuarioLogueado=Trabajador.objects.get(usuario=request.POST['Usuario'],psw=request.POST['Contrasena'])
                        UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
                        request.session['IdUsuario']=UsuarioLogueado.id
                        request.session['EstadoLogueo']=True
                        EstadoLogueo=True
                        NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
                        NombreOficina=UsuarioOficina.nombre
                        oficinas = Oficina.objects.all()
                        proveidos = Proveido.objects.all()
                        expediente = Expediente.objects.filter(estado="R")
                        return render_to_response('expedientes.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'EstadoLogueo':EstadoLogueo,'lista':expediente,'oficinas':oficinas,'proveidos':proveidos},context_instance=RequestContext(request))      
                    except ObjectDoesNotExist:
                        Info='Error, Su Usuario o Password Son Incorrectos'
                        Ctx={'Info':Info,'Form':Formulario}
                        return render_to_response('Logueo.html',Ctx,context_instance=RequestContext(request))
                else:
                    Info='Ingrese Sus Datos'
                    Ctx={'Info':Info,'Form':Formulario}
                    return render_to_response('Logueo.html',Ctx,context_instance=RequestContext(request))
            else:
                Formulario=LogueoNuevoForm()
                Info='else PPosts'
                Ctx={'Info':Info,'Form':Formulario}
                return render_to_response('Logueo.html',Ctx,context_instance=RequestContext(request))
    except:
        request.session['EstadoLogueo']=False
        Formulario=LogueoNuevoForm()
        Info='exception'
        Ctx={'Info':Info,'Form':Formulario}
        return render_to_response('Logueo.html',Ctx,context_instance=RequestContext(request))
