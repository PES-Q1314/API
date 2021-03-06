# -*- coding: utf-8 -*-
import datetime
from api import settings
from apps.base import enums
from apps.base.models import Departamento, ConocimientoTecnico, SectorDelMercado, Idioma, Especialidad
from apps.congelaciones.models import ModeloCongelable
from apps.denuncias.models import ModeloDenunciable, PerfilDenunciante
from apps.lista_negra.models import ModeloIncluibleEnLaListaNegra
from apps.suscripciones.models import PerfilSuscriptor
from django.db import models

import os
from model_utils.managers import InheritanceManager


def get_image_path(instance, filename):
    return os.path.join(instance.__class__.__name__, str(instance.id), filename)


class Perfil(ModeloDenunciable, ModeloCongelable, models.Model):
    """
    Perfil genérico de un usuario (asegura que solo pueda tener un perfil -Estudiante, Profesor, etc.)
    """
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='perfil')
    nombre = models.CharField(max_length=100, unique=True)

    objects = InheritanceManager()

    class Meta:
        db_table = 'Perfil'


class Estudiante(PerfilSuscriptor, PerfilDenunciante, Perfil):
    # Información personal
    dni = models.CharField(max_length=9, unique=True)
    fecha_de_nacimiento = models.DateField()
    foto_de_perfil = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=enums.SEXO)
    telefono = models.CharField(max_length=9, unique=True, blank=True, null=True)

    # Residencia
    direccion = models.CharField(max_length=200)
    latitud = models.FloatField()
    longitud = models.FloatField()

    # Currículo
    especialidad = models.ForeignKey(Especialidad)
    ultimo_curso_academico_superado = models.IntegerField(choices=enums.CURSO_ACADEMICO)
    descripcion = models.TextField(blank=True, null=True)
    conocimientos_tecnicos = models.ManyToManyField(ConocimientoTecnico,
                                                                through='EstudianteTieneConocimientoTecnico')
    experiencia_laboral = models.ManyToManyField(SectorDelMercado, through='EstudianteTieneExperienciaLaboral')
    idiomas = models.ManyToManyField(Idioma, through='EstudianteHablaIdioma')

    # Estado de búsqueda de trabajo
    busca_trabajo = models.BooleanField(default=False)
    disponibilidad = models.CharField(choices=enums.DISPONIBILIDAD, max_length=100, blank=True, null=True)

    # Metadatos del estudiante
    nivel_de_privacidad = models.CharField(choices=enums.NIVEL_DE_PRIVACIDAD, default='privado', max_length=100)

    class Meta:
        db_table = 'Estudiante'


class EstudianteTieneConocimientoTecnico(models.Model):
    estudiante = models.ForeignKey(Estudiante, related_name='conocimiento_tecnico_set')
    conocimiento = models.ForeignKey(ConocimientoTecnico)
    nivel = models.CharField(choices=enums.NIVEL_DE_CONOCIMIENTO, max_length=100)

    class Meta:
        db_table = 'EstudianteTieneConocimientoTecnico'


class EstudianteTieneExperienciaLaboral(models.Model):
    estudiante = models.ForeignKey(Estudiante, related_name='experiencia_laboral_set')
    sector = models.ForeignKey(SectorDelMercado)
    meses = models.IntegerField()

    class Meta:
        db_table = 'EstudianteTieneExperienciaLaboral'


class EstudianteHablaIdioma(models.Model):
    estudiante = models.ForeignKey(Estudiante, related_name='idioma_set')
    idioma = models.ForeignKey(Idioma)
    nivel = models.CharField(choices=enums.NIVEL_DE_CONOCIMIENTO, max_length=100)

    class Meta:
        db_table = 'EstudianteHablaIdioma'


class Profesor(Perfil, PerfilDenunciante):
    url_upc = models.URLField(unique=True)
    foto_de_perfil = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    departamento = models.ForeignKey(Departamento)

    class Meta:
        db_table = 'Profesor'


class Empresa(Perfil, ModeloIncluibleEnLaListaNegra, PerfilDenunciante):
    # Información de la empresa
    cif = models.CharField(max_length=9, unique=True)
    logotipo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    sector = models.ForeignKey(SectorDelMercado, blank=True, null=True)
    tamanyo = models.CharField(choices=enums.TAMANYO_DE_EMPRESA, max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    # Ubicación
    direccion = models.CharField(max_length=200, blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)

    # Metadatos de la empresa
    esta_activa = models.BooleanField(default=False)
    es_premium = models.BooleanField(default=False)
    fecha_de_finalizacion_de_cuenta_premium = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Empresa'

    def convertir_en_premium(self):
        self.es_premium = True
        self.fecha_de_finalizacion_de_cuenta_premium = datetime.datetime.today() + datetime.timedelta(weeks=52)
        self.save()

    def aceptar(self):
        self.esta_activa = True
        self.save()

    def rechazar(self):
        self.delete()


class Administrador(Perfil):
    class Meta:
        db_table = 'Administrador'


class Directivo(Perfil):
    class Meta:
        db_table = 'Directivo'

