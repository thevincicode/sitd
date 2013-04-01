# Create your views here.
from sitdapp.models import Expediente, ExpedienteTipo, Oficina,Trabajador, ExpedienteHistorial, Derivar, Proveido, Organizacion, Tupa, TupaRequisitos, TupaVinculo
from sitdapp.forms import TupaForm, TupaRequisitosForm, ExpedienteTipoForm, ProveidoForm, OrganizacionForm,LogueoNuevoForm,OficinaNuevoForm,TrabajadorNuevoForm, OficinaForm
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection, transaction
from django.contrib.auth.models import User
from django.template import RequestContext
from datetime import datetime, timedelta
from django.contrib import auth
from django.db.models import Q
import time
#ahora = str(datetime.now()) 


def expedientes(request):
    try: 
        if request.COOKIES.has_key( 'EstadoLogueo' ):
            value = request.COOKIES[ 'EstadoLogueo' ]
            if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
                UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
                UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
                NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
                NombreOficina=UsuarioOficina.nombre 
                empresa = Organizacion.objects.get(id=1)
                ahora = datetime.now().strftime("%d/%m/%Y")
                oficinas = Oficina.objects.all()
                proveidos = Proveido.objects.all()
                expediente = Expediente.objects.filter(oficina=UsuarioOficina).filter(Q(estado="R") | Q(estado="C"))
                if UsuarioLogueado.admin=="S":
                    expediente = Expediente.objects.filter(Q(estado="R") | Q(estado="C"))
                #expedientes=get_object_or_404(Expediente, estado=1)
                return render_to_response('expedientes.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'lista':expediente,'oficinas':oficinas,'proveidos':proveidos,'organizacion':empresa},context_instance=RequestContext(request))      
            else:
                html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
                return HttpResponse(html)
        else:
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
            return HttpResponse(html)
    except Exception, e:
        Formulario=LogueoNuevoForm()
        Info='exception '+ str(e)
        Ctx={'Info':Info,'Form':Formulario}
        return render_to_response('Logueo.html',Ctx,context_instance=RequestContext(request))

def expediente_registrar(request):
    try:
        if request.COOKIES.has_key( 'EstadoLogueo' ):
            value = request.COOKIES[ 'EstadoLogueo' ]
            if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
                UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
                UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
                NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
                NombreOficina=UsuarioOficina.nombre 
                empresa = Organizacion.objects.get(id=1)
                if request.method=="POST":                
                    nro = request.POST.get("nro")
                    tipos = request.POST.get("tipos")
                    codigo=request.POST.get("codigo")
                    folios=request.POST.get("folios")
                    interesado=request.POST.get("interesado")
                    fechar=request.POST.get("fechar")
                    asunto=request.POST.get("asunto")
                    tupa=request.POST.get("stupa")
                    destinatario=request.POST.get("destinatario")
                    #creando obj
                    tipo_obj=get_object_or_404(ExpedienteTipo, pk=tipos)
                    tupa_obj=get_object_or_404(Tupa,pk=tupa)
                    fechap= datetime.now()+timedelta(days=int(tupa_obj.tiempo))
                    try:
                        expediente_obj=Expediente(nro_exp=nro,nro_doc=codigo,folios=folios,interesado=interesado,asunto=asunto,destinatario=destinatario,f_inicio=datetime.now(),f_registro=datetime.now(),f_fint=fechap,observacion="",estado="C",tipo=tipo_obj,tupa=tupa_obj,oficina=UsuarioOficina,archivomotivo="",roficina=NombreOficina,rusuario=NombreUsuario)
                        expediente_obj.save()
                        print "guardo doc, intentando sacar ultimo id"
                        #mandando a imprimir
                        last=Expediente.objects.all().order_by('f_registro')
                        lon=len(last)
                        historial_last=last[lon-1]
                        lastid=historial_last.id
                        print "se guardo y el id fue: "+str(lastid)
                        link="/expediente/imprimir/"+str(lastid)
                        return HttpResponseRedirect(link)
                    except Exception, e:
                        html="error en "+str(e)
                        return HttpResponse(html)
                else:        
                    html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>No permitido</body></html>'
                    return HttpResponse(html)
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
            return HttpResponse(html)
    except Exception, e:
        Formulario=LogueoNuevoForm()
        Info='exception '+ str(e)
        Ctx={'Info':Info,'Form':Formulario}
        return render_to_response('Logueo.html',Ctx,context_instance=RequestContext(request))

def expediente_nuevo(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            if UsuarioLogueado.admin=="S":
                NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
                NombreOficina=UsuarioOficina.nombre 
                empresa = Organizacion.objects.get(id=1)
                tipo=ExpedienteTipo.objects.all()
                tupas=Tupa.objects.all()
                tupavinculo=TupaVinculo.objects.all()
                ahora = datetime.now().strftime("%d/%m/%Y")
                try:
                    last=Expediente.objects.all().order_by('f_registro')
                    lon=len(last)
                    historial_last=last[lon-1]
                    ultimonro=historial_last.nro_exp+1
                except Exception, e:
                    ultimonro=0
                return render_to_response('NuevoExpediente.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'tipo':tipo,'tupas':tupas,'tupavinculo':tupavinculo,'organizacion':empresa,'fechaserver':ahora,'ultimonro':ultimonro},context_instance=RequestContext(request))
            else:
                if UsuarioOficina.id==1:
                    NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
                    NombreOficina=UsuarioOficina.nombre 
                    empresa = Organizacion.objects.get(id=1)
                    tipo=ExpedienteTipo.objects.all()
                    tupas=Tupa.objects.all()
                    tupavinculo=TupaVinculo.objects.all()
                    ahora = datetime.now().strftime("%d/%m/%Y")
                    try:
                        last=Expediente.objects.all().order_by('f_registro')
                        lon=len(last)
                        historial_last=last[lon-1]
                        ultimonro=historial_last.nro_exp+1
                    except Exception, e:
                        ultimonro=0
                    return render_to_response('NuevoExpediente.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'tipo':tipo,'tupas':tupas,'tupavinculo':tupavinculo,'organizacion':empresa,'fechaserver':ahora,'ultimonro':ultimonro},context_instance=RequestContext(request))
                else:
                    html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Tramite Documentario acceder a ver esta opcion. <a href="/">Principal</a> </body></html>'
                    return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def archivados(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            ahora = datetime.now().strftime("%d/%m/%Y")
            oficinas = Oficina.objects.all()
            proveidos = Proveido.objects.all()
            expediente = Expediente.objects.filter(estado="A").filter(oficina=UsuarioOficina)
            if UsuarioLogueado.admin=="S":
                expediente = Expediente.objects.filter(estado="A")
            #expedientes=get_object_or_404(Expediente, estado=1)
            return render_to_response('archivados.html',{'organizacion':empresa,'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'lista':expediente,'oficinas':oficinas,'proveidos':proveidos},context_instance=RequestContext(request))
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def porrecibir(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            ahora = datetime.now().strftime("%d/%m/%Y")
            oficinas = Oficina.objects.all()
            proveidos = Proveido.objects.all()
            expediente = Expediente.objects.filter(estado="E").filter(oficina=UsuarioOficina)
            if UsuarioLogueado.admin=="S":
                expediente = Expediente.objects.filter(estado="E")
            #expedientes=get_object_or_404(Expediente, estado=1)
            return render_to_response('porrecibir.html',{'organizacion':empresa,'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'lista':expediente,'oficinas':oficinas,'proveidos':proveidos},context_instance=RequestContext(request))
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def expediente_detalle(request,id_expediente):
    try:    
        UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
        UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
        NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
        NombreOficina=UsuarioOficina.nombre 
        empresa = Organizacion.objects.get(id=1)
        expediente=get_object_or_404(Expediente, pk=id_expediente)
        historial=ExpedienteHistorial.objects.filter(expediente=expediente)
        return render_to_response('expediente_detalle.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'expediente':expediente, 'historial':historial},context_instance=RequestContext(request))
    except:
        NombreUsuario=""
        NombreOficina=""
        empresa = Organizacion.objects.get(id=1)
        expediente=get_object_or_404(Expediente, pk=id_expediente)
        historial=ExpedienteHistorial.objects.filter(expediente=expediente)
        return render_to_response('expediente_detalle.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'expediente':expediente, 'historial':historial},context_instance=RequestContext(request))

def expediente_imprimir(request,id_expediente):
    try:    
        UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
        UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
        NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
        NombreOficina=UsuarioOficina.nombre 
        empresa = Organizacion.objects.get(id=1)
        expediente=get_object_or_404(Expediente, pk=id_expediente)
        historial=ExpedienteHistorial.objects.filter(expediente=expediente)
        return render_to_response('imprimir.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'expediente':expediente},context_instance=RequestContext(request))
    except:
        NombreUsuario=""
        NombreOficina=""
        empresa = Organizacion.objects.get(id=1)
        expediente=get_object_or_404(Expediente, pk=id_expediente)
        historial=ExpedienteHistorial.objects.filter(expediente=expediente)
        return render_to_response('imprimir.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'expediente':expediente},context_instance=RequestContext(request))

def expediente_detalle_comentario(request,id_expediente,id_historial):
    try: 
        UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
        UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
        NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
        NombreOficina=UsuarioOficina.nombre 
        empresa = Organizacion.objects.get(id=1)   
        expediente=get_object_or_404(Expediente, pk=id_expediente)
        #historial=ExpedienteHistorial.objects.filter(expediente=expediente)
        historial=get_object_or_404(ExpedienteHistorial, pk=id_historial)
        return render_to_response('comentario.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'expediente':expediente, 'historial':historial},context_instance=RequestContext(request))
    except:
        NombreUsuario=""
        NombreOficina=""
        empresa = Organizacion.objects.get(id=1)   
        expediente=get_object_or_404(Expediente, pk=id_expediente)
        #historial=ExpedienteHistorial.objects.filter(expediente=expediente)
        historial=get_object_or_404(ExpedienteHistorial, pk=id_historial)
        return render_to_response('comentario.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'expediente':expediente, 'historial':historial},context_instance=RequestContext(request))


def buscador(request):
    if request.GET.get("b"):
        buscar = str(''+ request.GET["b"]+'')
        try:
            empresa = Organizacion.objects.get(id=1) 
            buscar=int(buscar)
            buscador=Expediente.objects.filter(nro_exp=buscar)
            return render_to_response('buscador.html',{'lista':buscador,'organizacion':empresa},context_instance=RequestContext(request))    
        except Exception, e:
            empresa = Organizacion.objects.get(id=1) 
            buscador=Expediente.objects.filter(interesado__contains=buscar)
            return render_to_response('buscador.html',{'lista':buscador,'organizacion':empresa},context_instance=RequestContext(request))    
            print "parametro a buscar es: " + buscar
            #buscar = '%r' % request.GET['b']
        
    else:
        html="<html><body>no envio ningun parametro</body></html>"
        return HttpResponse(html)

def expediente_derivar(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":            
            if request.method == "POST":
                id_s = request.POST.getlist("hi")
                comentario = request.POST.get('comentarioA','')
                oficina_s = request.POST.getlist("oficina")
                proveido_s = request.POST.getlist("proveido")
                print 'documentos ' + str(len(id_s))
                print 'oficinas ' + str(len(oficina_s))
                print 'proveidos ' + str(len(proveido_s))
                print 'el comentario fue: ' + comentario
                UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
                NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
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
                                idexpediente=v
                                expediente=get_object_or_404(Expediente, pk=idexpediente)
                                #generando un objeto de tipo Derivar y guardando
                                derivar_obj=Derivar(fecha=datetime.now(),estado="E",comentario=comentario,proveido=proveido,oficina=oficina,expediente=expediente)
                                derivar_obj.save()
                                print "se derivo"
                                #obteniendo el ultimo id registrado
                                id_derivar_obj=derivar_obj.id
                                #generando un objeto de tipo DerivarDetalle y guardando                        
                                oficina_o=expediente.oficina
                                #agregando al historial
                                historial_obj=ExpedienteHistorial(f_salida=datetime.now(),o_origen=oficina_o,o_destino=oficina.nombre,f_recepcion=datetime.now(),estado="enviado", proveido=proveido.nombre,expediente=expediente, ubicacion="-",comentario=comentario,usuario=NombreUsuario)
                                historial_obj.save()
                                print "se agrego al historial"
                                #actualizando estado del expediente
                                expediente_upd=Expediente.objects.get(pk=idexpediente)
                                expediente_upd.oficina=oficina
                                expediente_upd.estado="E"
                                expediente_upd.save()
                                #expediente_upd.estado="E"
                                print "se actualizo la oficina del expediente"
                                #expediente_upd.save()
                                html='<html><head><meta http-equiv="Refresh" content="2;url=/"></head><body>Los datos fueron registrados <a href="/">aqui</a></body></html>'
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
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def expediente_archivar(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            if request.method == "POST":
                UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])
                UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
                NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
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
                            #agrando estado archivado
                            last=Derivar.objects.filter(expediente=expediente_upd).order_by('fecha')
                            lon=len(last)
                            try:
                                historial_last=last[lon-1]
                                derivar_obj=Derivar(fecha=datetime.now(),estado="A",comentario=comentario,proveido=historial_last.proveido,oficina=UsuarioOficina,expediente=expediente_upd)
                                derivar_obj.save()
                                print "se archivo en Derivados"
                                #agregando al historial
                                historial_obj=ExpedienteHistorial(f_salida=datetime.now(),o_origen=historial_last.oficina,o_destino=UsuarioOficina.nombre,f_recepcion=datetime.now(),estado="Archivado", proveido=historial_last.proveido,expediente=expediente_upd, ubicacion="-",comentario=comentario,usuario=NombreUsuario)
                                historial_obj.save()
                            except Exception, e:
                                proveido=Proveido.objects.get(pk=1)
                                derivar_obj=Derivar(fecha=datetime.now(),estado="A",comentario=comentario,proveido=proveido,oficina=UsuarioOficina,expediente=expediente_upd)
                                derivar_obj.save()
                                print "se archivo en Derivados por defecto"
                                #agregando al historial
                                historial_obj=ExpedienteHistorial(f_salida=datetime.now(),o_origen=UsuarioOficina,o_destino=UsuarioOficina,f_recepcion=datetime.now(),estado="Archivado", proveido=proveido.nombre,expediente=expediente_upd, ubicacion="-",comentario=comentario,usuario=NombreUsuario)
                                historial_obj.save()
                            html='<html><head><meta http-equiv="Refresh" content="2;url=/archivados"></head><body>Los datos fueron registrados <a href="/archivados">aqui</a></body></html>'
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
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def expediente_recibir(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            if request.method == "POST":
                UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])
                UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
                NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
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
                            print "se recibio R del expediente"
                            #buscando el ultimo movimiento
                            last=ExpedienteHistorial.objects.filter(expediente=expediente_upd).order_by('f_salida')
                            lon=len(last)
                            historial_last=last[lon-1]
                            historial_obj=ExpedienteHistorial(f_salida=datetime.now(),o_origen=historial_last.o_origen,o_destino=expediente_upd.oficina.nombre,f_recepcion=datetime.now(),estado="Recibido", proveido=historial_last.proveido,expediente=expediente_upd, ubicacion="-",comentario="recibido",usuario=NombreUsuario)
                            historial_obj.save()

                            last2=Derivar.objects.filter(expediente=expediente_upd).order_by('fecha')
                            lon2=len(last2)
                            historial_last2=last2[lon2-1]
                            derivar_obj=Derivar(fecha=datetime.now(),estado="R",comentario="Recibido",proveido=historial_last2.proveido,oficina=UsuarioOficina,expediente=expediente_upd)
                            derivar_obj.save()
                            print "se recibio en Derivados"

                            html='<html><head><meta http-equiv="Refresh" content="2;url=/bandeja"></head><body>Los datos fueron registrados <a href="/bandeja">aqui</a></body></html>'
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
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

# el famoso tupa
def tupa_lista(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])  
            if UsuarioLogueado.admin=="S":
                UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
                NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
                NombreOficina=UsuarioOficina.nombre 
                empresa = Organizacion.objects.get(id=1)
                ahora = datetime.now().strftime("%d/%m/%Y")
                tupa=Tupa.objects.all()
                return render_to_response('tupa_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':tupa},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def tupa_nuevo(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                if request.method=='POST':
                    formulario=TupaForm(request.POST)
                    if formulario.is_valid():
                        formulario.save()
                        return HttpResponseRedirect('/tupa')
                else:
                    formulario=TupaForm()
                return render_to_response('tupaform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def tupa_editar(request, id_tupa):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)   
            if UsuarioLogueado.admin=="S":
                tupa=get_object_or_404(Tupa,pk=id_tupa)
                formulario=TupaForm(request.POST or None, instance=tupa)
                if formulario.is_valid():
                    formulario.save()
                    return HttpResponseRedirect('/tupa')
                return render_to_response('tupaform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)            
   
def tupa_eliminar(request,id_tupa):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)   
            if UsuarioLogueado.admin=="S":
                try:
                    tupa=Tupa.objects.get(pk=id_tupa)
                    tupa.delete()
                    return HttpResponse('delete')
                except Exception, e:
                    raise e
                    return HttpResponseRedirect('/tupa')
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

#requisitos del tupa
def tuparequisitos_lista(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)  
            tupa=TupaRequisitos.objects.all()
            if UsuarioLogueado.admin=="S":
                return render_to_response('tuparequisitos_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':tupa},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def tuparequisitos_nuevo(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)  
            if UsuarioLogueado.admin=="S": 
                if request.method=='POST':
                    formulario=TupaRequisitosForm(request.POST)
                    if formulario.is_valid():
                        formulario.save()
                        return HttpResponseRedirect('/tupa/requisitos')
                else:
                    formulario=TupaRequisitosForm()
                return render_to_response('tuparequisitosform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def tuparequisitos_editar(request, id_requisito):   
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                tupa=get_object_or_404(TupaRequisitos,pk=id_requisito)
                formulario=TupaRequisitosForm(request.POST or None, instance=tupa)
                if formulario.is_valid():
                    formulario.save()
                    return HttpResponseRedirect('/tupa/requisitos')
                return render_to_response('tuparequisitosform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

   
def tuparequisitos_eliminar(request,id_requisito):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                try:
                    tupa=TupaRequisitos.objects.get(pk=id_requisito)
                    tupa.delete()
                    return HttpResponse('delete')
                except Exception, e:
                    raise e
                    return HttpResponseRedirect('/tupa/requisitos')
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)


#vincular el tupa con sus requisitos
def tupavincular(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":                 
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
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def tupavinculo_nuevo(request, id_tupa):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S": 
                tupa=get_object_or_404(Tupa,pk=id_tupa)
                requisitos=TupaRequisitos.objects.all()
                return render_to_response('tupavinculo.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'tupa':tupa,'requisitos':requisitos},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def tupavinculo_listar(request, id_tupa):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                tupas=get_object_or_404(Tupa,pk=id_tupa)
                vinculo=TupaVinculo.objects.filter(tupa=tupas)
                #requisitos=TupaRequisitos.objects.filter(id=vinculo.requisitos)
                return render_to_response('tupavinculo_detalle.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'tupas':tupas,'requisitos':vinculo},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def tupavinculo_editarguardar(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            if UsuarioLogueado.admin=="S":   
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
                                html='<html><head><meta http-equiv="Refresh" content="3;url=/tupa/"></head><body>Los Datos Fueron vinculados <a href="/tupa/">Tupas</a> </body></html>'
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
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def tupavinculo_editar(request, id_tupa):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                tupa=get_object_or_404(Tupa,pk=id_tupa)
                requisitos=TupaRequisitos.objects.all()
                return render_to_response('tupavinculo_editar.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'tupa':tupa,'requisitos':requisitos},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def tupavinculo_eliminar(request,id_tupa):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            try:
                if UsuarioLogueado.admin=="S":
                    tupas=get_object_or_404(Tupa,pk=id_tupa)
                    vinculo=TupaVinculo.objects.filter(tupa=tupas)
                    vinculo.delete()
                    return HttpResponse('delete')
                else:        
                    html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                    return HttpResponse(html)    
            except Exception, e:
                raise e
                return HttpResponseRedirect('/tupa/requisitos')
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

# proveidos
def proveido_lista(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                tupa=Proveido.objects.all()
                return render_to_response('proveido_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':tupa},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def proveido_nuevo(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                if request.method=='POST':
                    formulario=ProveidoForm(request.POST)
                    if formulario.is_valid():
                        formulario.save()
                        return HttpResponseRedirect('/proveidos')
                else:
                    formulario=ProveidoForm()
                return render_to_response('proveidoform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def proveido_editar(request, id_proveido): 
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)  
            if UsuarioLogueado.admin=="S":
                tupa=get_object_or_404(Proveido,pk=id_proveido)
                formulario=ProveidoForm(request.POST or None, instance=tupa)
                if formulario.is_valid():
                    formulario.save()
                    return HttpResponseRedirect('/proveidos')
                return render_to_response('proveidoform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)
   
def proveido_eliminar(request,id_proveido):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            try:
                if UsuarioLogueado.admin=="S":
                    proveido=Proveido.objects.get(pk=id_proveido)
                    proveido.delete()
                    return HttpResponse('delete')
                else:        
                    html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                    return HttpResponse(html)
            except Exception, e:
                raise e
                return HttpResponseRedirect('/proveidos')
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

# tipos de expedientes
def expedientetipo_lista(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                tupa=ExpedienteTipo.objects.all()
                return render_to_response('expedientetipo_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':tupa},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def expedientetipo_nuevo(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                if request.method=='POST':
                    formulario=ExpedienteTipoForm(request.POST)
                    if formulario.is_valid():
                        formulario.save()
                        return HttpResponseRedirect('/expediente/tipos')
                else:
                    formulario=ExpedienteTipoForm()
                return render_to_response('expedientetipoform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def expedientetipo_editar(request, id_tipo):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":   
                tupa=get_object_or_404(Proveido,pk=id_tipo)
                formulario=ExpedienteTipoForm(request.POST or None, instance=tupa)
                if formulario.is_valid():
                    formulario.save()
                    return HttpResponseRedirect('/expediente/tipos')
                return render_to_response('expedientetipoform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)
   
def expedientetipo_eliminar(request,id_tipo):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            try:
                if UsuarioLogueado.admin=="S":
                    exptipo=ExpedienteTipo.objects.get(pk=id_tipo)
                    exptipo.delete()
                    return HttpResponse('delete')
                else:        
                    html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                    return HttpResponse(html)
            except Exception, e:
                raise e
                return HttpResponseRedirect('/expediente/tipos')
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def organizacion_listar(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                organizacion=Organizacion.objects.all()
                return render_to_response('organizacion_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':organizacion},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def organizacion_editar(request, id_org):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                organizacion=get_object_or_404(Organizacion,pk=id_org)
                formulario=OrganizacionForm(request.POST or None,instance=organizacion) 
                if formulario.is_valid():
                    formulario.save()
                    return HttpResponseRedirect('/organizacion')
                return render_to_response('organizacionform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

#sergio
def TrabajadorControl(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                Lista=Trabajador.objects.all()
                Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Form':Lista}
                return render_to_response('TrabajadorControl.html',Ctx,context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def TrabajadorNuevo(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                if request.method=='POST':
                    Info='Inicializando'
                    Formulario=TrabajadorNuevoForm(request.POST)
                    if Formulario.is_valid():
                        try:
                            Formulario.save()
                            Info='Se registro Nuevo Trabajador'
                            Lista=Trabajador.objects.all()
                            Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Info':Info,'Form':Lista}
                            return render_to_response('TrabajadorControl.html',Ctx,context_instance=RequestContext(request))
                        except:
                            Info='Error, El Dni Ingresado Ya Existe'
                            Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Info':Info,'Form':Formulario}
                            return render_to_response('TrabajadorNuevo.html',Ctx,context_instance=RequestContext(request))
                    else:
                        Info='Ingrese toda la informacion solicitada'
                        Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Info':Info,'Form':Formulario}
                        return render_to_response('TrabajadorNuevo.html',Ctx,context_instance=RequestContext(request))
                else:
                    Info='Ingrese la informacion requerida'
                    Formulario=TrabajadorNuevoForm()
                    Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Form':Formulario,'Info':Info}
                    return render_to_response('TrabajadorNuevo.html',Ctx,context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def TrabajadorEliminarDesicion(request,id_trabajador):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                EliminarTrabajador=Trabajador.objects.get(pk=id_trabajador)
                Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'id_trabajador':id_trabajador,'Trabajador':EliminarTrabajador}
                return render_to_response('TrabajadorEliminar.html',Ctx,context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def trabajador_editar(request, id_trabajador):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            EditarTrabajador=Trabajador.objects.get(pk=id_trabajador)
            if UsuarioLogueado.admin=="S":
                #formulario=OrganizacionForm(request.POST or None,instance=organizacion) 
                #if formulario.is_valid():
                 #   formulario.save()
                  #  return HttpResponseRedirect('/organizacion')
                #return render_to_response('organizacionform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request)) 
                Info='Inicializando'
                Formulario=TrabajadorNuevoForm(request.POST or None,instance=EditarTrabajador)
                if Formulario.is_valid():
                    try:
                        Formulario.save()
                        return HttpResponseRedirect('/TrabajadorControl')
                    except:
                        html='<html><head><meta http-equiv="Refresh" content="3;url=/OficinaControl"></head><body>Error de parametro exception</body></html>'
                        return HttpResponse(html)
                return render_to_response('trabajadoreditar.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':Formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def TrabajadorEliminar(request,id_trabajador):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                try:
                    '''ALguna Restriccion'''
                    EliminarTrabajador=Trabajador.objects.get(pk=id_trabajador)
                    EliminarTrabajador.delete()
                    Info='Se Elimino el trabajador: '+EliminarTrabajador.nombre+' '+EliminarTrabajador.apellidos
                    Lista=Trabajador.objects.all()
                    Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Info':Info,'Form':Lista}
                    return render_to_response('TrabajadorControl.html',Ctx,context_instance=RequestContext(request))
                except ObjectDoesNotExist:
                    EliminarTrabajador=Trabajador.objects.get(pk=id_trabajador)
                    EliminarTrabajador.delete()
                    Info='Se Elimino el trabajador: '+EliminarTrabajador.nombre+' '+EliminarTrabajador.apellidos
                    Lista=Trabajador.objects.all()
                    ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Info':Info,'Form':Lista}
                    return render_to_response('TrabajadorControl.html',Ctx,context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def OficinaEliminarDesicion(request,id_oficina):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                EliminarOficina=Oficina.objects.get(pk=id_oficina)
                Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'id_oficina':id_oficina,'Oficina':EliminarOficina}
                return render_to_response('OficinaEliminar.html',Ctx,context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def OficinaEliminar(request,id_oficina):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                try:
                    EliminarTrabajador=Trabajador.objects.get(oficina_id=id_oficina)
                    Info='Error, No se puede eliminar la oficina La oficina ya esta asignado a un trabajador'
                    Lista=Oficina.objects.all()
                    Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Form':Lista,'Info':Info}
                    return render_to_response('OficinaControl.html',Ctx,context_instance=RequestContext(request))
                    
                except ObjectDoesNotExist:
                    EliminarOficina=Oficina.objects.get(pk=id_oficina)
                    EliminarOficina.delete()
                    Info='Se Elimino la oficina de '+EliminarOficina.nombre
                    Lista=Oficina.objects.all()
                    Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Form':Lista,'Info':Info}
                    return render_to_response('OficinaControl.html',Ctx,context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def OficinaControl(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
                Lista=Oficina.objects.all()
                Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Form':Lista}
                return render_to_response('OficinaControl.html',Ctx,context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def oficina_editar(request, id_oficina):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ": 
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            EditarOficina=Oficina.objects.get(pk=id_oficina)
            #formulario=OrganizacionForm(request.POST or None,instance=organizacion) 
            #if formulario.is_valid():
             #   formulario.save()
              #  return HttpResponseRedirect('/organizacion')
            #return render_to_response('organizacionform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':formulario},context_instance=RequestContext(request)) 
            if UsuarioLogueado.admin=="S":
                Info='Inicializando'
                Formulario=OficinaForm(request.POST or None,instance=EditarOficina)
                if Formulario.is_valid():
                    try:
                        Formulario.save()
                        return HttpResponseRedirect('/OficinaControl')
                    except:
                        html='<html><head><meta http-equiv="Refresh" content="3;url=/OficinaControl"></head><body>Error de parametro exception</body></html>'
                        return HttpResponse(html)
                return render_to_response('oficinaform.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'formulario':Formulario},context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def OficinaNuevo(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if UsuarioLogueado.admin=="S":
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
                            Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Form':Lista,'Info':Info}
                            return render_to_response('OficinaControl.html',Ctx,context_instance=RequestContext(request))
                        except:
                            Info='Error, El Nombre Ingresado Ya Existe'
                            Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Info':Info,'Form':Formulario}
                            return render_to_response('OficinaNuevo.html',Ctx,context_instance=RequestContext(request))
             
                    else:
                        Info='Ingrese Toda la Infomacion Solicitada'
                        Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Info':Info,'Form':Formulario}
                        return render_to_response('OficinaNuevo.html',Ctx,context_instance=RequestContext(request))
                else:
                    Formulario=OficinaNuevoForm()
                    Ctx={'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Form':Formulario}
                    return render_to_response('OficinaNuevo.html',Ctx,context_instance=RequestContext(request))
            else:        
                html='<html><head><meta http-equiv="Refresh" content="3;url=/"></head><body>Solo Administradores pueden ver esta opcion. <a href="/">Principal</a> </body></html>'
                return HttpResponse(html)
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def LogueoSalir(request):
    response = HttpResponseRedirect("/Logueo")
    response.delete_cookie('EstadoLogueo')
    response.delete_cookie('IdUsuario')
    return response

def LogueoNuevo(request):
    try:
        if request.COOKIES.has_key( 'EstadoLogueo' ):
            value = request.COOKIES[ 'EstadoLogueo' ]
            if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
                UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
                UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
                NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
                NombreOficina=UsuarioOficina.nombre
                empresa = Organizacion.objects.get(id=1)
                ahora = datetime.now().strftime("%d/%m/%Y")
                oficinas = Oficina.objects.all()
                proveidos = Proveido.objects.all()
                expediente = Expediente.objects.filter(oficina=UsuarioOficina).filter(Q(estado="R") | Q(estado="C"))
                if UsuarioLogueado.admin=="S":
                    expediente = Expediente.objects.filter(Q(estado="R") | Q(estado="C"))
                return render_to_response('expedientes.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'lista':expediente,'oficinas':oficinas,'proveidos':proveidos,'organizacion':empresa},context_instance=RequestContext(request))      
        else:
            if request.method=='POST':
                Info='Inicializando'
                Formulario=LogueoNuevoForm(request.POST)
                if Formulario.is_valid():
                    try:
                        UsuarioLogueado=Trabajador.objects.get(usuario=request.POST['Usuario'],psw=request.POST['Contrasena'])
                        UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
                        #request.session['IdUsuario']=UsuarioLogueado.id
                        #request.session['EstadoLogueo']=True
                        #EstadoLogueo=True
                        NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
                        NombreOficina=UsuarioOficina.nombre
                        empresa = Organizacion.objects.get(id=1)
                        ahora = datetime.now().strftime("%d/%m/%Y")
                        oficinas = Oficina.objects.all()
                        proveidos = Proveido.objects.all()
                        expediente = Expediente.objects.filter(oficina=UsuarioOficina).filter(Q(estado="R") | Q(estado="C"))
                        if UsuarioLogueado.admin=="S":
                            expediente = Expediente.objects.filter(Q(estado="R") | Q(estado="C"))
                        response=render_to_response('expedientes.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'lista':expediente,'oficinas':oficinas,'proveidos':proveidos,'organizacion':empresa},context_instance=RequestContext(request))      
                        response.set_cookie( 'EstadoLogueo', 'Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ' )
                        response.set_cookie( 'IdUsuario',  UsuarioLogueado.id )
                        return response
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
                Info='Ingrese su informacion'
                Ctx={'Info':Info,'Form':Formulario}
                return render_to_response('Logueo.html',Ctx,context_instance=RequestContext(request))
    except Exception, e:
        request.session['EstadoLogueo']=False
        Formulario=LogueoNuevoForm()
        Info='Ingrese su informacion'
        Ctx={'Info':Info,'Form':Formulario}
        return render_to_response('Logueo.html',Ctx,context_instance=RequestContext(request))

def reportes(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            try:
                UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
                UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
                NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
                NombreOficina=UsuarioOficina.nombre 
                empresa = Organizacion.objects.get(id=1)
                return render_to_response('reportes.html', {'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa}, context_instance=RequestContext(request))
            except:
                NombreUsuario=""
                NombreOficina=""
                empresa = Organizacion.objects.get(id=1)
                return render_to_response('reportes.html', {'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa}, context_instance=RequestContext(request))
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)

def reportes_fechas(request):
    if request.COOKIES.has_key( 'EstadoLogueo' ):
        value = request.COOKIES[ 'EstadoLogueo' ]
        if value=="Y3n1K0pSnlf3v7FdKRYaY5UdYvAfsYqZ":
            UsuarioLogueado=Trabajador.objects.get(id=request.COOKIES[ 'IdUsuario' ])   
            UsuarioOficina=Oficina.objects.get(id=UsuarioLogueado.oficina_id)
            NombreUsuario=UsuarioLogueado.nombre+' '+UsuarioLogueado.apellidos
            NombreOficina=UsuarioOficina.nombre 
            empresa = Organizacion.objects.get(id=1)
            if request.GET.get("opcion"):
                opcion = int(request.GET["opcion"])
                print "opcion  "+str(opcion)
                intervalo=int(request.GET["intervalo"])
                print "intervalo "+str(intervalo)
                fecha1=request.GET["fecha1"]
                print "fecha1 "+fecha1
                fecha2=request.GET["fecha2"]
                print "fecha2 "+fecha2
                if opcion==1:
                    if intervalo==1:
                        try:
                            titulo="DOCUMENTOS RECIBIDOS HOY("+datetime.now().strftime("%d-%m-%Y")+")"
                            print titulo
                            start_date=datetime.now().strftime("%d/%m/%Y") 
                            start_date=datetime.strptime(start_date, "%d/%m/%Y")
                            print str(start_date)
                            end_date = start_date+timedelta(days=1)
                            print str(end_date)
                            recibidos=Derivar.objects.filter(Q(estado="R") | Q(estado="C")).filter(fecha__range=(start_date, end_date)).filter(oficina=UsuarioOficina)
                            return render_to_response('reportes_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':recibidos,'titulo':titulo},context_instance=RequestContext(request))
                        except Exception, e:
                            html="<html><body> Excepcion <br>"+str(e)+"</body></html>"
                            return HttpResponse(html)
                    elif intervalo==2:               
                        titulo="DOCUMENTOS RECIBIDOS ENTRE ("+fecha1+" - "+fecha2+")"
                        start_date=datetime.strptime(fecha1, "%d/%m/%Y")
                        end_date=datetime.strptime(fecha2, "%d/%m/%Y")
                        recibidos=Derivar.objects.filter(estado="R").filter(oficina=UsuarioOficina)
                        return render_to_response('reportes_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':recibidos,'titulo':titulo},context_instance=RequestContext(request))
                    else:
                        html="<html><body>Error de Intervalo</body></html>"
                        return HttpResponse(html)
                elif opcion==2:
                    if intervalo==1:
                        titulo="DOCUMENTOS DERIVADOS HOY("+datetime.now().strftime("%d-%m-%Y")+")"
                        start_date=datetime.now().strftime("%d/%m/%Y") 
                        start_date=datetime.strptime(start_date, "%d/%m/%Y")
                        end_date = start_date+timedelta(days=1)
                        recibidos=Derivar.objects.filter(estado="E").filter(fecha__range=(start_date, end_date)).filter(oficina=UsuarioOficina)
                        return render_to_response('reportes_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':recibidos,'titulo':titulo},context_instance=RequestContext(request))
                    
                    elif intervalo==2:               
                        titulo="DOCUMENTOS DERIVADOS ENTRE ("+fecha1+" - "+fecha2+")"
                        start_date=datetime.strptime(fecha1, "%d/%m/%Y")
                        end_date=datetime.strptime(fecha2, "%d/%m/%Y")
                        recibidos=Derivar.objects.filter(estado="E").filter(oficina=UsuarioOficina)
                        return render_to_response('reportes_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':recibidos,'titulo':titulo},context_instance=RequestContext(request))
                    else:
                        html="<html><body>Error de Intervalo</body></html>"
                        return HttpResponse(html)
                elif opcion==3:
                    if intervalo==1:
                        titulo="DOCUMENTOS ARCHIVADOS HOY("+datetime.now().strftime("%d/%m/%Y")+")"
                        start_date=datetime.now().strftime("%d/%m/%Y") 
                        start_date=datetime.strptime(start_date, "%d/%m/%Y")
                        end_date = start_date+timedelta(days=1)
                        recibidos=Derivar.objects.filter(estado="A").filter(fecha__range=(start_date, end_date)).filter(oficina=UsuarioOficina)
                        return render_to_response('reportes_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':recibidos,'titulo':titulo},context_instance=RequestContext(request))
                    
                    elif intervalo==2:               
                        titulo="DOCUMENTOS ARCHIVADOS ENTRE ("+fecha1+" - "+fecha2+")"
                        start_date=datetime.strptime(fecha1, "%d/%m/%Y")
                        end_date=datetime.strptime(fecha2, "%d/%m/%Y")
                        recibidos=Derivar.objects.filter(estado="R").filter(oficina=UsuarioOficina)
                        return render_to_response('reportes_lista.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'lista':recibidos,'titulo':titulo},context_instance=RequestContext(request))
                    else:
                        html="<html><body>Error de Intervalo</body></html>"
                        return HttpResponse(html)
                elif opcion==4:
                    if intervalo==1:
                        titulo="MONTO ACUMULADO HOY("+datetime.now().strftime("%d-%m-%Y")+")"
                        start_date=datetime.now().strftime("%d-%m-%Y") 
                        start_date=datetime.strptime(start_date, "%d-%m-%Y")
                        end_date = start_date+timedelta(days=1)
                        recibidos=Expediente.objects.filter(f_registro__range=(start_date, end_date))
                        Suma=0
                        for Item in recibidos:
                            Suma=Suma+Item.tupa.valor 
                        return render_to_response('ReporteTotal.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Suma':Suma,'titulo':titulo},context_instance=RequestContext(request))
                    
                    elif intervalo==2:            
                        titulo="MONTO ACUMULADO ENTRE ("+fecha1+" - "+fecha2+")"
                        start_date=datetime.strptime(fecha1, "%d/%m/%Y")
                        end_date=datetime.strptime(fecha2, "%d/%m/%Y")
                        recibidos=Expediente.objects.filter(f_registro__range=(start_date, end_date))
                        Suma=0
                        for Item in recibidos:
                            Suma=Suma+Item.tupa.valor 
                        return render_to_response('ReporteTotal.html',{'NombreUsuario':NombreUsuario,'NombreOficina':NombreOficina,'organizacion':empresa,'Suma':Suma,'titulo':titulo},context_instance=RequestContext(request))
                    else:
                        html="<html><body>Error de Intervalo</body></html>"
                        return HttpResponse(html)
                else:       
                    html="<html><body>Error de opcion</body></html>"
                    return HttpResponse(html)
               
            else:       
                html="<html><body>No se envio parametros</body></html>"
                return HttpResponse(html)    
        else:        
            html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Error de parametro En el Login</body></html>'
            return HttpResponse(html)
    else:        
        html='<html><head><meta http-equiv="Refresh" content="3;url=/Logueo"></head><body>Logueese en el sistema para tener acceso <a href="/Logueo">aqui</a></body></html>'
        return HttpResponse(html)


