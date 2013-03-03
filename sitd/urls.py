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
    url(r'^derivar/$', 'sitdapp.views.expediente_derivar'),
    url(r'^archivar/$', 'sitdapp.views.expediente_archivar'),
    url(r'^archivados/$', 'sitdapp.views.archivados'),
    url(r'^bandeja/$', 'sitdapp.views.porrecibir'),
    url(r'^recibir/$', 'sitdapp.views.expediente_recibir'),
    #url(r'^$','sitdapp.views.login'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
