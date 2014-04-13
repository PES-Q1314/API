# coding=utf-8
from apps.base import enums
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ModeloSuscribible(models.Model):
    suscripciones = GenericRelation('Suscripcion', content_type_field='modelo_ct', object_id_field='modelo_oid')

    class Meta:
        abstract = True


class PerfilSuscriptor(models.Model):
    suscripciones = GenericRelation('Suscripcion', content_type_field='autor_ct', object_id_field='autor_oid')

    class Meta:
        abstract = True


class Suscripcion(models.Model):
    # Apuntador genérico a Modelos Suscribibles
    modelo_ct = models.ForeignKey(ContentType, related_name='modelo_suscripciones')
    modelo_oid = models.PositiveIntegerField()
    modelo = GenericForeignKey('modelo_ct', 'modelo_oid')

    # Apuntador genérico a Perfiles Suscriptores
    autor_ct = models.ForeignKey(ContentType, related_name='autor_suscripciones')
    autor_oid = models.PositiveIntegerField()
    autor = GenericForeignKey('autor_ct', 'autor_oid')

    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(choices=enums.ESTADO_DE_LA_SUSCRIPCION, default='pendiente', max_length=20)

    class Meta:
        db_table = 'Suscripcion'



