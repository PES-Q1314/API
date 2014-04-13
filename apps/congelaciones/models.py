# coding=utf-8
from apps.base import enums
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ModeloCongelable(models.Model):
    congelaciones = GenericRelation('Congelacion')
    fecha_de_ultima_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def fecha_de_ultima_congelacion(self):
        return self.congelaciones.all().order_by('-fecha').first()

    @property
    def ha_sido_modificado_tras_una_congelacion(self):
        return self.fecha_de_ultima_congelacion < self.fecha_de_ultima_modificacion


class Congelacion(models.Model):
    # Apuntador genérico a Modelos Congelables
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    modelo = GenericForeignKey()

    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=140)
    estado = models.CharField(choices=enums.ESTADO_DE_LA_CONGELACION, default='pendiente', max_length=20)

    class Meta:
        db_table = 'Congelacion'


