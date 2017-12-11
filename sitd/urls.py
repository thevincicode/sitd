from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import sitdapp.views
import os
#import django.contrib.auth.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()
urlpatterns = [
    path('', sitdapp.views.expedientes),
    path('expediente/nuevo', sitdapp.views.expediente_nuevo),
    path('expediente/registrar', sitdapp.views.expediente_registrar),
    re_path('expediente/(?P<id_expediente>\d+)',
            sitdapp.views.expediente_detalle),
    re_path('expediente/imprimir/(?P<id_expediente>\d+)',
            sitdapp.views.expediente_imprimir),
    re_path('expediente/(?P<id_expediente>\d+)/comentario/(?P<id_historial>\d+)',
            sitdapp.views.expediente_detalle_comentario),
    path('derivar', sitdapp.views.expediente_derivar),
    path('archivar', sitdapp.views.expediente_archivar),
    path('archivados', sitdapp.views.archivados),
    path('bandeja', sitdapp.views.porrecibir),
    path('recibir', sitdapp.views.expediente_recibir),
    path('buscar', sitdapp.views.buscador),
    path('tupa', sitdapp.views.tupa_lista),
    path('tupa/nuevo', sitdapp.views.tupa_nuevo),
    re_path('tupa/editar/(?P<id_tupa>\d+)', sitdapp.views.tupa_editar),
    re_path('tupa/eliminar/(?P<id_tupa>\d+)', sitdapp.views.tupa_eliminar),
    path('tupa/requisitos', sitdapp.views.tuparequisitos_lista),
    path('tupa/requisitos/nuevo', sitdapp.views.tuparequisitos_nuevo),
    re_path('tupa/requisitos/editar/(?P<id_requisito>\d+)',
            sitdapp.views.tuparequisitos_editar),
    re_path('tupa/requisitos/eliminar/(?P<id_requisito>\d+)',
            sitdapp.views.tuparequisitos_eliminar),
    path('tupa/vincular/', sitdapp.views.tupavincular),
    re_path('tupa/vinculo/(?P<id_tupa>\d+)',
            sitdapp.views.tupavinculo_listar),
    re_path('tupa/vincular/nuevo/(?P<id_tupa>\d+)',
            sitdapp.views.tupavinculo_nuevo),
    re_path('tupa/vincular/editar/(?P<id_tupa>\d+)',
            sitdapp.views.tupavinculo_editar),
    path('tupa/vincular/editarguardar',
         sitdapp.views.tupavinculo_editarguardar),
    re_path('tupa/vincular/eliminar/(?P<id_tupa>\d+)',
            sitdapp.views.tupavinculo_eliminar),
    path('proveidos', sitdapp.views.proveido_lista),
    path('proveido/nuevo', sitdapp.views.proveido_nuevo),
    re_path('proveido/editar/(?P<id_proveido>\d+)',
            sitdapp.views.proveido_editar),
    re_path('proveido/eliminar/(?P<id_proveido>\d+)',
            sitdapp.views.proveido_eliminar),
    path('expediente/tipos', sitdapp.views.expedientetipo_lista),
    path('expediente/tipo/nuevo', sitdapp.views.expedientetipo_nuevo),
    re_path('expediente/tipo/editar/(?P<id_tipo>\d+)',
            sitdapp.views.expedientetipo_editar),
    re_path('expediente/tipo/eliminar/(?P<id_tipo>\d+)',
            sitdapp.views.expedientetipo_eliminar),
    path('organizacion/', sitdapp.views.organizacion_listar),
    re_path('organizacion/editar/(?P<id_org>\d+)',
            sitdapp.views.organizacion_editar),
    path('reportes', sitdapp.views.reportes),
    path('reporte', sitdapp.views.reportes_fechas),
    # aca esta de sergio
    path('Logueo', sitdapp.views.LogueoNuevo),
    path('LogueoSalir', sitdapp.views.LogueoSalir),
    path('OficinaNuevo', sitdapp.views.OficinaNuevo),
    path('OficinaControl', sitdapp.views.OficinaControl),
    re_path('OficinaEliminar/(?P<id_oficina>\d+)',
            sitdapp.views.OficinaEliminar),
    re_path('Oficina/editar/(?P<id_oficina>\d+)',
            sitdapp.views.oficina_editar),
    re_path('OficinaEliminarDesicion/(?P<id_oficina>\d+)',
            sitdapp.views.OficinaEliminarDesicion),
    path('TrabajadorNuevo', sitdapp.views.TrabajadorNuevo),
    path('TrabajadorControl', sitdapp.views.TrabajadorControl),
    re_path('TrabajadorEliminar/(?P<id_trabajador>\d+)',
            sitdapp.views.TrabajadorEliminar),
    re_path('trabajador/editar/(?P<id_trabajador>\d+)',
            sitdapp.views.trabajador_editar),
    re_path('TrabajadorEliminarDesicion/(?P<id_trabajador>\d+)',
            sitdapp.views.TrabajadorEliminarDesicion),

    path('admin/doc', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    re_path('carga/(?P<path>.*)', serve,
            {'document_root': settings.MEDIA_ROOT, }
            )
]

urlpatterns += staticfiles_urlpatterns()
