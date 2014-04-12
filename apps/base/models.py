# -*- coding: utf-8 -*-
from apps.base.datos.idiomas import ISO_639_1
from django.db import models



class Idioma(models.Model):
    """ Idioma, siguiendo la ISO 639-1 """
    codigo = models.CharField(max_length=2, choices=ISO_639_1)
    idioma = models.CharField(max_length=40)


class ConocimientoTecnico(models.Model):
    conocimiento = models.CharField()


class SectorDelMercado(models.Model):
    sector = models.CharField()


class Departamento(models.Model):
    siglas = models.CharField()
    nombre = models.CharField()
    url_upc = models.URLField()

