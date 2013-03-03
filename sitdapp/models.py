from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.

class Calendario(models.Model):
	dia=models.CharField(max_length=15, verbose_name=u'dia de la semana', help_text='lunes, martes..')
	fecha=models.DateField()
	estado=models.BooleanField(verbose_name='laborable',help_text='laborable o feriado')
	descripcion=models.TextField(max_length=250,verbose_name='(Opcional)')	
	
	def __unicode__(self):
			return self.dia

class Oficina(models.Model):
	nombre=models.CharField(max_length=75, verbose_name='Nombre',unique=True,help_text='Nombre del Pais')
	descripcion=models.TextField(max_length=250, verbose_name='Descripcion')

	def __unicode__(self):
			return self.nombre

class Formulario(models.Model):
	nombre=models.CharField(max_length=25)
	descripcion=models.TextField(max_length=50)

	def __unicode__(self):
		return self.nombre
		
class Trabajador(models.Model):
	dni=models.CharField(max_length=8, unique=True)
	nombre=models.CharField(max_length=100)
	apellidos=models.CharField(max_length=250)
	f_nacimiento=models.DateField(verbose_name=u'Fecha de Nacimiento')
	cargo=models.CharField(max_length=25)
	usuario=models.CharField(max_length=25)
	psw=models.CharField(max_length=25)
	oficina=models.ForeignKey(Oficina)

	def __unicode__(self):
			return self.dni

class TrabajadorHistorial(models.Model):
	fecha=models.DateField()
	oficina=models.CharField(max_length=25)
	echo=models.CharField(max_length=25)
	trabajador=models.ForeignKey(Trabajador)


class TrabajadorPersmisos(models.Model):
	nuevo=models.BooleanField(default=1,verbose_name='nuevo',help_text='permisos para crear nuevo')
	eliminar=models.BooleanField(default=1,verbose_name='eliminar',help_text='permisos para eliminar')
	modificar=models.BooleanField(default=1,verbose_name='modificar',help_text='permisos para modificar')
	imprimir=models.BooleanField(default=1,verbose_name='imprimir',help_text='permisos para imprimir')
	formulario=models.ForeignKey(Formulario)
	trabajador=models.ForeignKey(Trabajador)


class TupaRequisitos(models.Model):
	requisito=models.CharField(max_length=45)
	descripcion=models.TextField(max_length=150)

	def __unicode__(self):
			return self.requisito

class Tupa(models.Model):
	denominacion=models.CharField(max_length=25)
	descripcion=models.TextField(max_length=75)
	autoridad=models.TextField(max_length=75)
	porcentaje=models.DecimalField(max_digits=10,decimal_places=2)
	valor=models.DecimalField(max_digits=10,decimal_places=3)
	tiempo=models.IntegerField()

	def __unicode__(self):
			return self.denominacion

class TupaVinculo(models.Model):
	tupa=models.ForeignKey(Tupa)
	requisitos=models.ForeignKey(TupaRequisitos)


class ExpedienteTipo(models.Model):
	nombre=models.CharField(max_length=25)
	descripcion=models.TextField(max_length=75)

	def __unicode__(self):
			return self.nombre

class Expediente(models.Model):
	GENDER_CHOICES = (
        ('E', 'Enviado'),
        ('R', 'Recivido'),
        ('A', 'Archivado'),
    )
	nro_exp=models.IntegerField(verbose_name=u'Numero de Expediente')
	nro_doc=models.CharField(max_length=25)
	folios=models.IntegerField()
	interesado=models.CharField(max_length=55)
	asunto=models.CharField(max_length=80)
	destinatario=models.CharField(max_length=80)
	f_inicio=models.DateField(verbose_name=u'Fecha de Inicio')
	f_registro=models.DateField(verbose_name=u'Fecha de Registro')
	f_fint=models.DateField(verbose_name=u'Fecha de fin del tramite')
	observacion=models.TextField(max_length=150)
	estado=models.CharField(max_length=1,choices=GENDER_CHOICES)
	tipo=models.ForeignKey(ExpedienteTipo)
	tupa=models.ForeignKey(Tupa)
	oficina=models.ForeignKey(Oficina)
	nota=models.TextField(max_length=150)

	def __unicode__(self):
			return self.nro_doc

class Proveido(models.Model):
	nombre=models.CharField(max_length=250)
	descripcion=models.TextField(max_length=350)
	
	def __unicode__(self):
			return self.nombre

class Derivar(models.Model):
	GENDER_CHOICES = (
        ('E', 'Enviado'),
        ('R', 'Recivido'),
        ('A', 'Archivado'),
    )
	fecha=models.DateField()
	estado=models.CharField(max_length=1,choices=GENDER_CHOICES)
	comentario=models.TextField(max_length=150)
	proveido=models.ForeignKey(Proveido)
	oficina=models.ForeignKey(Oficina)

class DerivarDetalle(models.Model):
	fecha=models.DateField()
	expediente=models.ForeignKey(Expediente)
	derivar=models.ForeignKey(Derivar)


class ExpedienteHistorial(models.Model):
	f_salida=models.DateField(verbose_name=u'Fecha de Salida')
	o_origen=models.CharField(max_length=50, verbose_name=u'Oficina de origen')
	o_destino=models.CharField(max_length=50, verbose_name=u'Ofina de destino')
	f_recepcion=models.DateField(verbose_name=u'Fecha de recepcion')
	estado=models.CharField(max_length=250)
	proveido=models.CharField(max_length=250)
	expediente=models.ForeignKey(Expediente)
	ubicacion=models.CharField(max_length=150)