# coding=utf-8
from apps.base import enums
from apps.base.models import ConocimientoTecnico, SectorDelMercado, Idioma, Especialidad
from apps.congelaciones.models import ModeloCongelable
from apps.denuncias.models import ModeloDenunciable
from apps.suscripciones.models import ModeloSuscribible
from apps.usuarios.models import Empresa, Profesor, Estudiante, Perfil
from django.db import models
from model_utils.managers import InheritanceManager


class Oferta(ModeloDenunciable, ModeloCongelable, ModeloSuscribible, models.Model):
    # Características de la oferta
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=600)
    puesto = models.CharField(max_length=150, blank=True, null=True)
    meses_de_duracion = models.IntegerField(blank=True, null=True)
    fecha_de_incorporacion = models.DateField()
    numero_de_puestos_vacantes = models.IntegerField()
    horario = models.CharField(choices=enums.HORARIO_DE_TRABAJO, max_length=50)
    tipo_de_jornada = models.CharField(choices=enums.JORNADA_LABORAL, max_length=50)

    especialidades = models.ManyToManyField(Especialidad, related_name='none+')
    ultimo_curso_academico_superado = models.IntegerField(choices=enums.CURSO_ACADEMICO, blank=True, null=True)
    requisitos_de_conocimiento_tecnico = models.ManyToManyField(ConocimientoTecnico,
                                                                through='RequisitoDeConocimientoTecnico')
    requisitos_de_experiencia_laboral = models.ManyToManyField(SectorDelMercado, through='RequisitoDeExperienciaLaboral')
    requisitos_de_idioma = models.ManyToManyField(Idioma, through='RequisitoDeIdioma')

    # Ubicación
    direccion = models.CharField(max_length=200, blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)

    # Metadatos de la oferta
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)

    objects = InheritanceManager()

    class Meta:
        db_table = 'Oferta'



class RequisitoDeConocimientoTecnico(models.Model):
    oferta = models.ForeignKey(Oferta, related_name='requisito_de_conocimiento_tecnico_set')
    conocimiento = models.ForeignKey(ConocimientoTecnico)
    nivel = models.CharField(choices=enums.NIVEL_DE_CONOCIMIENTO, max_length=50)

    class Meta:
        db_table = 'RequisitoDeConocimientoTecnico'


class RequisitoDeExperienciaLaboral(models.Model):
    oferta = models.ForeignKey(Oferta, related_name='requisito_de_experiencia_laboral_set')
    sector = models.ForeignKey(SectorDelMercado)
    meses = models.IntegerField()

    class Meta:
        db_table = 'RequisitoDeExperienciaLaboral'


class RequisitoDeIdioma(models.Model):
    oferta = models.ForeignKey(Oferta, related_name='requisito_de_idioma_set')
    idioma = models.ForeignKey(Idioma)
    nivel = models.CharField(choices=enums.NIVEL_DE_CONOCIMIENTO, max_length=50)

    class Meta:
        db_table = 'RequisitoDeIdioma'


class OfertaDeEmpresa(Oferta):
    usuario = models.ForeignKey(Empresa)
    hay_posibilidad_de_tfg = models.BooleanField(default=False)
    salario_mensual = models.IntegerField(blank=True, null=True)
    persona_de_contacto = models.CharField(max_length=100, blank=True, null=True)
    email_de_contacto = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = 'OfertaDeEmpresa'


class OfertaDeDepartamento(Oferta):
    usuario = models.ForeignKey(Profesor)

    class Meta:
        db_table = 'OfertaDeDepartamento'


class OfertaDeProyectoEmprendedor(Oferta):
    usuario = models.ForeignKey(Estudiante)

    class Meta:
        db_table = 'OfertaDeProyectoEmprendedor'