# -*- coding: utf-8 -*-
from apps.base.datos.idiomas import ISO_639_1
from django.db import models



class Idioma(models.Model):
    """ Idioma, siguiendo la ISO 639-1 """
    codigo = models.CharField(max_length=2)
    idioma = models.CharField(max_length=50)

    class Meta:
        db_table = 'Idioma'
        unique_together = ('codigo', 'idioma')


class ConocimientoTecnico(models.Model):
    conocimiento = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'ConocimientoTecnico'


class SectorDelMercado(models.Model):
    sector = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'Sector'


class Departamento(models.Model):
    siglas = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50)
    url_upc = models.URLField()

    class Meta:
        db_table = 'Departamento'
        unique_together = ('siglas', 'nombre')


class Especialidad(models.Model):
    nombre = models.CharField(max_length=50)
    facultad = models.CharField(max_length=50)
    url_upc = models.URLField()

    class Meta:
        db_table = 'Especialidad'
        unique_together = ('nombre', 'facultad')
