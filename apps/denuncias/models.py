# coding=utf-8
from apps.base import enums
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ModeloDenunciable(models.Model):
    denuncias = GenericRelation('Denuncia')

    class Meta:
        abstract = True


class PerfilDenunciante(models.Model):
    denuncias = GenericRelation('Denuncia', content_type_field='denunciante_ct', object_id_field='denunciante_oid')
    notificar_cambio_de_estado_de_la_denuncia = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Denuncia(models.Model):
    # Apuntador genérico a Modelos Denunciables
    content_type = models.ForeignKey(ContentType, related_name='none+')
    object_id = models.PositiveIntegerField()
    modelo = GenericForeignKey()

    # Apuntador genérico a Perfiles Denunciantes
    denunciante_ct = models.ForeignKey(ContentType, related_name='none+')
    denunciante_oid = models.PositiveIntegerField()
    denunciante = GenericForeignKey('denunciante_ct', 'denunciante_oid')

    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=140)
    estado = models.CharField(choices=enums.ESTADO_DE_LA_DENUNCIA, default='pendiente', max_length=20)

    class Meta:
        db_table = 'Denuncia'



