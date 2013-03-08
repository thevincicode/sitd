from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sitd.views.home', name='home'),
    # url(r'^sitd/', include('sitd.foo.urls')),

    url(r'^$','sitdapp.views.expedientes'),
    url(r'^expediente/(?P<id_expediente>\d+)$','sitdapp.views.expediente_detalle'),
    url(r'^expediente/(?P<id_expediente>\d+)/comentario/(?P<id_historial>\d+)$','sitdapp.views.expediente_detalle_comentario'),
    url(r'^derivar/$', 'sitdapp.views.expediente_derivar'),
    url(r'^archivar/$', 'sitdapp.views.expediente_archivar'),
    url(r'^archivados/$', 'sitdapp.views.archivados'),
    url(r'^bandeja/$', 'sitdapp.views.porrecibir'),
    url(r'^recibir/$', 'sitdapp.views.expediente_recibir'),
    url(r'^buscar/$','sitdapp.views.buscador'),
    url(r'^tupa/$','sitdapp.views.tupa_lista'),
    url(r'^tupa/nuevo$','sitdapp.views.tupa_nuevo'),
    url(r'^tupa/editar/(?P<id_tupa>\d+)$','sitdapp.views.tupa_editar'),
    url(r'^tupa/eliminar/(?P<id_tupa>\d+)$','sitdapp.views.tupa_eliminar'),
    url(r'^tupa/requisitos/$','sitdapp.views.tuparequisitos_lista'),
    url(r'^tupa/requisitos/nuevo$','sitdapp.views.tuparequisitos_nuevo'),
    url(r'^tupa/requisitos/editar/(?P<id_requisito>\d+)$','sitdapp.views.tuparequisitos_editar'),
    url(r'^tupa/requisitos/eliminar/(?P<id_requisito>\d+)$','sitdapp.views.tuparequisitos_eliminar'),
    url(r'^tupa/vincular$','sitdapp.views.tupavincular'),
    url(r'^tupa/vinculo/(?P<id_tupa>\d+)$','sitdapp.views.tupavinculo_listar'),
    url(r'^tupa/vincular/nuevo/(?P<id_tupa>\d+)$','sitdapp.views.tupavinculo_nuevo'),
    url(r'^tupa/vincular/editar/(?P<id_tupa>\d+)$','sitdapp.views.tupavinculo_editar'),
    url(r'^tupa/vincular/editarguardar$','sitdapp.views.tupavinculo_editarguardar'),
    url(r'^tupa/vincular/eliminar/(?P<id_tupa>\d+)$','sitdapp.views.tupavinculo_eliminar'),
    url(r'^proveidos/$','sitdapp.views.proveido_lista'),
    url(r'^proveido/nuevo$','sitdapp.views.proveido_nuevo'),
    url(r'^proveido/editar/(?P<id_proveido>\d+)$','sitdapp.views.proveido_editar'),
    url(r'^proveido/eliminar/(?P<id_proveido>\d+)$','sitdapp.views.proveido_eliminar'),
    url(r'^expediente/tipos$','sitdapp.views.expedientetipo_lista'),
    url(r'^expediente/tipo/nuevo$','sitdapp.views.expedientetipo_nuevo'),
    url(r'^expediente/tipo/editar/(?P<id_tipo>\d+)$','sitdapp.views.expedientetipo_editar'),
    url(r'^expediente/tipo/eliminar/(?P<id_tipo>\d+)$','sitdapp.views.expedientetipo_eliminar'),
    url(r'^organizacion/$','sitdapp.views.organizacion_listar'),
    url(r'^organizacion/editar/(?P<id_org>\d+)$','sitdapp.views.organizacion_editar'),
    #aca esta de sergio
    url(r'^Logueo/$', 'sitdapp.views.LogueoNuevo'),
    url(r'^LogueoSalir/$', 'sitdapp.views.LogueoSalir'),
    url(r'^OficinaNuevo/$','sitdapp.views.OficinaNuevo'),
    url(r'^OficinaControl/$','sitdapp.views.OficinaControl'),
    url(r'^OficinaEliminar/(?P<id_oficina>\d+)$','sitdapp.views.OficinaEliminar'),
    url(r'^OficinaEliminarDesicion/(?P<id_oficina>\d+)$','sitdapp.views.OficinaEliminarDesicion'),
    url(r'^TrabajadorNuevo/$','sitdapp.views.TrabajadorNuevo'),
    url(r'^TrabajadorControl/$','sitdapp.views.TrabajadorControl'),
    url(r'^TrabajadorEliminar/(?P<id_trabajador>\d+)$','sitdapp.views.TrabajadorEliminar'),
    url(r'^TrabajadorEliminarDesicion/(?P<id_trabajador>\d+)$','sitdapp.views.TrabajadorEliminarDesicion'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^carga/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,}
        ),
)
