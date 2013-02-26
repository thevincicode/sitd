from sitdapp.models import Calendario, Oficina, Formulario, Trabajador, TrabajadorHistorial, TrabajadorPersmisos, TupaRequisitos, Tupa, TupaVinculo, ExpedienteEstado, ExpedienteTipo, Expediente, Proveido, Derivar, DerivarDetalle, ExpedienteHistorial
from django.contrib import admin

class ExpedienteAdmin(admin.ModelAdmin):
	list_display=('nro_exp','nro_doc')
	search_fields=('nro_exp','nro_doc')

admin.site.register(Calendario)
admin.site.register(Oficina)
admin.site.register(Formulario)
admin.site.register(Trabajador)
admin.site.register(TrabajadorHistorial)
admin.site.register(TrabajadorPersmisos)
admin.site.register(TupaRequisitos)
admin.site.register(Tupa)
admin.site.register(TupaVinculo)
admin.site.register(ExpedienteEstado)
admin.site.register(ExpedienteTipo)
admin.site.register(Expediente)
admin.site.register(Proveido)
admin.site.register(Derivar)
admin.site.register(DerivarDetalle)
admin.site.register(ExpedienteHistorial)