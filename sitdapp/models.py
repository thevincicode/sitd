# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.


class Calendario(models.Model):
    dia = models.CharField(
        max_length=15, verbose_name=u'dia de la semana', help_text='lunes, martes..')
    fecha = models.DateTimeField()
    estado = models.BooleanField(
        verbose_name='laborable', help_text='laborable o feriado')
    descripcion = models.TextField(
        max_length=250, verbose_name='(Opcional)', blank=True)

    def __unicode__(self):
        return self.dia


class Oficina(models.Model):
    nombre = models.CharField(
        max_length=75, verbose_name='Nombre', unique=True, help_text='Nombre de la Oficina')
    descripcion = models.TextField(
        max_length=250, verbose_name='Descripcion', blank=True)

    def __unicode__(self):
        return self.nombre


class Formulario(models.Model):
    nombre = models.CharField(max_length=25)
    descripcion = models.TextField(max_length=50, blank=True)

    def __unicode__(self):
        return self.nombre


class Trabajador(models.Model):
    GENDER_CHOICES = (
        ('N', 'NO'),
        ('S', 'SI'),
    )
    dni = models.CharField(max_length=8, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=250)
    f_nacimiento = models.DateField(
        verbose_name=u'Fecha de Nacimiento', help_text='dias/mes/año')
    cargo = models.CharField(max_length=25)
    usuario = models.CharField(max_length=25, unique=True)
    psw = models.CharField(max_length=25, verbose_name=u'PASSWORD')
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE)
    admin = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __unicode__(self):
        return self.dni


class TrabajadorHistorial(models.Model):
    fecha = models.DateTimeField()
    oficina = models.CharField(max_length=25)
    echo = models.CharField(max_length=25)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)


class TrabajadorPersmisos(models.Model):
    nuevo = models.BooleanField(
        default=1, verbose_name='nuevo', help_text='permisos para crear nuevo')
    eliminar = models.BooleanField(
        default=1, verbose_name='eliminar', help_text='permisos para eliminar')
    modificar = models.BooleanField(
        default=1, verbose_name='modificar', help_text='permisos para modificar')
    imprimir = models.BooleanField(
        default=1, verbose_name='imprimir', help_text='permisos para imprimir')
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)


class TupaRequisitos(models.Model):
    requisito = models.CharField(max_length=45)
    descripcion = models.TextField(max_length=150)

    def __unicode__(self):
        return self.requisito


class Tupa(models.Model):
    denominacion = models.CharField(max_length=85)
    descripcion = models.TextField(max_length=275, blank=True)
    autoridad = models.TextField(max_length=175)
    porcentaje = models.DecimalField(max_digits=10, decimal_places=2)
    valor = models.DecimalField(max_digits=10, decimal_places=3)
    tiempo = models.IntegerField()

    def __unicode__(self):
        return self.denominacion


class TupaVinculo(models.Model):
    tupa = models.ForeignKey(Tupa, on_delete=models.CASCADE)
    requisitos = models.ForeignKey(TupaRequisitos, on_delete=models.CASCADE)


class ExpedienteTipo(models.Model):
    nombre = models.CharField(max_length=25)
    descripcion = models.TextField(max_length=75, blank=True)

    def __unicode__(self):
        return self.nombre


class Expediente(models.Model):
    GENDER_CHOICES = (
        ('C', 'Creado'),
        ('E', 'Enviado'),
        ('R', 'Recivido'),
        ('A', 'Archivado'),
    )
    nro_exp = models.IntegerField(verbose_name=u'Numero de Expediente')
    nro_doc = models.CharField(max_length=95, verbose_name=u'codigo externo')
    folios = models.IntegerField()
    interesado = models.CharField(max_length=155)
    asunto = models.CharField(max_length=180)
    destinatario = models.CharField(max_length=180)
    f_inicio = models.DateTimeField(verbose_name=u'Fecha de Inicio')
    f_registro = models.DateTimeField(verbose_name=u'Fecha de Registro')
    f_fint = models.DateTimeField(verbose_name=u'Fecha de fin del tramite')
    observacion = models.TextField(max_length=150)
    estado = models.CharField(max_length=1, choices=GENDER_CHOICES)
    tipo = models.ForeignKey(ExpedienteTipo, on_delete=models.CASCADE)
    tupa = models.ForeignKey(Tupa, on_delete=models.CASCADE)
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE)
    archivomotivo = models.TextField(max_length=1500)
    roficina = models.CharField(
        max_length=250, verbose_name=u'Oficina donde se registro')
    rusuario = models.CharField(
        max_length=250, verbose_name=u'Usuario que registro')

    def __unicode__(self):
        return self.nro_doc


class Proveido(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(max_length=350, blank=True)

    def __unicode__(self):
        return self.nombre


class Derivar(models.Model):
    GENDER_CHOICES = (
        ('C', 'Creado'),
        ('E', 'Enviado'),
        ('R', 'Recibido'),
        ('A', 'Archivado'),
    )
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=1, choices=GENDER_CHOICES)
    comentario = models.TextField(max_length=150, blank=True)
    proveido = models.ForeignKey(Proveido, on_delete=models.CASCADE)
    oficina = models.ManyToManyField(
        Oficina, blank=True, editable=False, related_name='%(app_label)s_%(class)s_destino')
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    oficinao = models.ManyToManyField(
        Oficina, blank=True, editable=False, related_name='%(app_label)s_%(class)s_origen')


class ExpedienteHistorial(models.Model):
    f_salida = models.DateTimeField(verbose_name=u'Fecha de Salida')
    o_origen = models.CharField(
        max_length=50, verbose_name=u'Oficina de origen')
    o_destino = models.CharField(
        max_length=50, verbose_name=u'Ofina de destino')
    f_recepcion = models.DateTimeField(verbose_name=u'Fecha de recepcion')
    estado = models.CharField(max_length=250)
    proveido = models.CharField(max_length=250)
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=150)
    comentario = models.TextField(
        max_length=1000, verbose_name=u'Comentario', help_text='maximo 1000 caracteres', blank=True)
    usuario = models.CharField(max_length=500)


class Organizacion(models.Model):
    nombre = models.CharField(
        max_length=500, verbose_name=u'Nombre de la Institucion')
    logo = models.ImageField(upload_to='Imagen', verbose_name='Imagen logo')
    direccion = models.CharField(
        max_length=850, verbose_name=u'direccion', blank=True)

    def __unicode__(self):
        return self.nombre
