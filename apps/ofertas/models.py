# coding=utf-8
from apps.base import enums
from apps.base.models import ConocimientoTecnico, SectorDelMercado, Idioma
from apps.suscripciones.models import ModeloSuscribible
from apps.usuarios.models import Empresa, Profesor, Estudiante
from django.db import models


class Oferta(ModeloSuscribible, models.Model):
    # Características de la oferta
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=600)
    meses_de_duracion = models.IntegerField()
    fecha_de_incorporacion = models.DateField()
    numero_de_puestos_vacantes = models.IntegerField()
    horario = models.CharField(choices=enums.HORARIO_DE_TRABAJO, max_length=20)
    requisitos_de_conocimiento_tecnico = models.ManyToManyField(ConocimientoTecnico,
                                                                through='RequisitoDeConocimientoTecnico')
    requisitos_de_experiencia_laboral = models.ManyToManyField(SectorDelMercado, through='RequisitoDeExperienciaLaboral')
    requisitos_de_idioma = models.ManyToManyField(Idioma, through='RequisitoDeIdioma')
    # TODO: ubicacion

    # Metadatos de la oferta
    # TODO: Averiguar como es posible obligar a que las subclases de Oferta implementen
    # una foreign key a una subclase de Perfil, y el campo de la FK se llame 'autor'
    # TODO: Abstraer elementos congelables
    fecha_de_creacion = models.DateTimeField(auto_now_add=True)
    fecha_de_ultima_congelacion = models.DateTimeField()
    motivo_de_la_congelacion = models.CharField(max_length=140)
    fecha_de_ultima_modificacion = models.DateTimeField()

    # class Meta:
    # TODO: Editar los metadatos de este y el resto de modelos para especificar
    # un nombre concreto con el que la tabla se guardará en la BD

    @property
    def tipo_de_jornada(self):
        if self.horario == 'total':
            return 'completa'
        else:
            return 'parcial'


class RequisitoDeConocimientoTecnico(models.Model):
    oferta = models.ForeignKey(Oferta)
    conocimiento = models.ForeignKey(ConocimientoTecnico)
    nivel = models.CharField(choices=enums.NIVEL_DE_CONOCIMIENTO, max_length=20)


class RequisitoDeExperienciaLaboral(models.Model):
    oferta = models.ForeignKey(Oferta)
    sector = models.ForeignKey(SectorDelMercado)
    meses = models.IntegerField()


class RequisitoDeIdioma(models.Model):
    oferta = models.ForeignKey(Oferta)
    idioma = models.ForeignKey(Idioma)
    nivel = models.CharField(choices=enums.NIVEL_DE_CONOCIMIENTO, max_length=20)

# TODO: Revalorar el hecho de que una oferta sea abstracta, para poder hacer
# que la oferta genérica sea un ModeloSuscribible en sí misma
class OfertaDeEmpresa(Oferta):
    # TODO: En este y otros modelos, marcar como ', blank=True, null=True' aquellos campos que puedan quedar vacíos
    autor = models.ForeignKey(Empresa)
    ultimo_curso_academico_superado = models.IntegerField(choices=enums.CURSO_ACADEMICO)
    hay_posibilidad_de_tfg = models.BooleanField()
    salario_mensual = models.IntegerField()
    persona_de_contacto = models.CharField(max_length=100)
    email_de_contacto = models.EmailField()


class OfertaDeDepartamento(Oferta):
    autor = models.ForeignKey(Profesor)


class OfertaDeProyectoEmprendedor(Oferta):
    autor = models.ForeignKey(Estudiante)