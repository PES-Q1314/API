# coding=utf-8
from apps.base import enums
from core.modelo import resolver_usuario
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ModeloSuscribible(models.Model):
    suscripciones = GenericRelation('Suscripcion', content_type_field='modelo_ct', object_id_field='modelo_oid')

    class Meta:
        abstract = True

    def suscripcion_del_usuario(self, usuario):
        u_ct = ContentType.objects.get_for_model(usuario)
        s = self.suscripciones.filter(suscriptor_ct__pk=u_ct.pk, suscriptor_oid=usuario.id)
        return s.first() if s.exists() else None


class PerfilSuscriptor(models.Model):
    suscripciones = GenericRelation('Suscripcion', content_type_field='suscriptor_ct', object_id_field='suscriptor_oid')

    # Notificaciones relacionadas con modelos suscribibles
    notificar_cambio_de_estado_de_la_suscripcion = models.BooleanField(default=True)
    recibe_el_boletin_semanal = models.BooleanField(default=True)
    recibe_ofertas_personalizadas = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Suscripcion(models.Model):
    # Apuntador genérico a Modelos Suscribibles
    modelo_ct = models.ForeignKey(ContentType, related_name='none+')
    modelo_oid = models.PositiveIntegerField()
    modelo = GenericForeignKey('modelo_ct', 'modelo_oid')

    # Apuntador genérico a Perfiles Suscriptores
    suscriptor_ct = models.ForeignKey(ContentType, related_name='none+')
    suscriptor_oid = models.PositiveIntegerField()
    suscriptor = GenericForeignKey('suscriptor_ct', 'suscriptor_oid')

    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(choices=enums.ESTADO_DE_LA_SUSCRIPCION, default='pendiente', max_length=20)

    class Meta:
        db_table = 'Suscripcion'

    class YaValorada(Exception):
        pass

    class MismoUsuario(Exception):
        pass

    def save(self, *args, **kwargs):
        if resolver_usuario(self.modelo) == resolver_usuario(self.suscriptor):
            raise Suscripcion.MismoUsuario
        super().save(*args, **kwargs)

    def delete(self, using=None):
        if self.estado != 'pendiente':
            raise Suscripcion.YaValorada()
        else:
            super().delete()





