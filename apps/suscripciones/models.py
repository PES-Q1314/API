# coding=utf-8
from apps.base import enums
from apps.usuarios.models import Estudiante
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ModeloSuscribible(models.Model):
    suscripciones = GenericRelation('Suscripcion')

    class Meta:
        abstract = True


class Suscripcion(models.Model):
    # Apuntador genérico a Modelos Suscribibles
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    modelo = GenericForeignKey()

    estudiante = models.ForeignKey(Estudiante, related_name='suscripciones')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(choices=enums.ESTADO_DE_LA_SUSCRIPCION, max_length=20)



