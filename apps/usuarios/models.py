# -*- coding: utf-8 -*-
from api import settings
from apps.base import enums
from apps.base.models import Departamento, ConocimientoTecnico, SectorDelMercado, Idioma
from django.db import models

import os

# TODO: Mejorar este modelo para abstraer el nombre del modelo y poder usar el mismo método en todas
def get_image_path(instance, filename):
    return os.path.join('estudiante', str(instance.id), filename)


class Perfil(models.Model):
    """
    Perfil genérico de un usuario (asegura que solo pueda tener un perfil -Estudiante, Profesor, etc.)
    """
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='perfil')
    nombre = models.CharField(max_length=100)


class Estudiante(Perfil):
    # Información personal
    dni = models.CharField(max_length=9)
    fecha_de_nacimiento = models.DateField()
    foto_de_perfil = models.ImageField(upload_to=get_image_path)
    sexo = models.CharField(max_length=1, choices=enums.SEXO)
    telefono = models.CharField(max_length=9)
    # TODO: incluir residencia (openmaps?)

    # Currículo
    # TODO: incluir en los perfiles y en otras partes del proyecto los estudios cursados por la persona
    ultimo_curso_academico_superado = models.IntegerField(choices=enums.CURSO_ACADEMICO)
    descripcion = models.TextField()
    conocimientos_tecnicos = models.ManyToManyField(ConocimientoTecnico,
                                                                through='XConocimientoTecnico')
    experiencia_laboral = models.ManyToManyField(SectorDelMercado, through='XExperienciaLaboral')
    idiomas = models.ManyToManyField(Idioma, through='XIdioma')

    # Estado de búsqueda de trabajo
    busca_trabajo = models.BooleanField()
    disponibilidad = models.CharField(choices=enums.DISPONIBILIDAD, max_length=20)

    # Metadatos del estudiante
    nivel_de_privacidad = models.CharField(choices=enums.NIVEL_DE_PRIVACIDAD, max_length=20)


# TODO: Refactorizar estas tres tablas y ponerles un nombre más semántico
class XConocimientoTecnico(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    conocimiento = models.ForeignKey(ConocimientoTecnico)
    nivel = models.CharField(choices=enums.NIVEL_DE_CONOCIMIENTO, max_length=20)


class XExperienciaLaboral(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    sector = models.ForeignKey(SectorDelMercado)
    meses = models.IntegerField()


class XIdioma(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    idioma = models.ForeignKey(Idioma)
    nivel = models.CharField(choices=enums.NIVEL_DE_CONOCIMIENTO, max_length=20)



class Profesor(Perfil):
    url_upc = models.URLField()
    foto_de_perfil = models.ImageField(upload_to=get_image_path)
    departamento = models.ForeignKey(Departamento)


class Empresa(Perfil):
    # Información de la empresa
    cif = models.CharField(max_length=9)
    logotipo = models.ImageField(upload_to=get_image_path)
    sector = models.ForeignKey(SectorDelMercado)
    tamanyo = models.CharField(choices=enums.TAMANYO_DE_EMPRESA, max_length=20)
    descripcion = models.TextField()

    # Metadatos de la empresa
    esta_activa = models.BooleanField(default=False)
    es_premium = models.BooleanField(default=False)
    fecha_de_finalizacion_de_cuenta_premium = models.DateField()
    fecha_de_ultima_congelacion = models.DateTimeField()
    motivo_de_la_congelacion = models.CharField(max_length=140)
    fecha_de_ultima_modificacion = models.DateTimeField()


