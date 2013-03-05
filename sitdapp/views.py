# Create your views here.
from sitdapp.models import Expediente, Oficina,Trabajador, ExpedienteHistorial, Derivar, DerivarDetalle ,Proveido
from django.db import connection, transaction
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from datetime import datetime

def expedientes(request):
	#ahora = datetime.datetime.now() today = datetime.now()
    oficinas = Oficina.objects.all()
    proveidos = Proveido.objects.all()
    expediente = Expediente.objects.filter(estado="R")
	#expedientes=get_object_or_404(Expediente, estado=1)
    return render_to_response('expedientes.html',{'lista':expediente,'oficinas':oficinas,'proveidos':proveidos},context_instance=RequestContext(request))

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
        comentario = request.POST.get('comentario','')
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
                        derivar_obj=Derivar(fecha="2013-01-02",estado="E",comentario=comentario,proveido=proveido,oficina=oficina)
                        derivar_obj.save()
                        print "se derivo"
                        #obteniendo el ultimo id registrado
                        id_derivar_obj=derivar_obj.id
                        #generando un objeto de tipo DerivarDetalle y guardando
                        idexpediente=v
                        expediente=get_object_or_404(Expediente, pk=idexpediente)
                        derivar=get_object_or_404(Derivar, pk=id_derivar_obj)
                        derivardetalle_obj=DerivarDetalle(fecha="2013-01-02", expediente=expediente, derivar=derivar)
                        derivardetalle_obj.save()
                        print "se derivo completo "
                        oficina_o=expediente.oficina
                        #agregando al historial
                        historial_obj=ExpedienteHistorial(f_salida="2013-01-02",o_origen=oficina_o,o_destino=oficina.nombre,f_recepcion="2013-01-02",estado="enviado", proveido=proveido.nombre,expediente=expediente, ubicacion="-")
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
       

