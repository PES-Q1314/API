# coding=utf-8
from apps.base import enums
from apps.ofertas.models import Oferta
from apps.usuarios.models import Perfil
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class VisitaAOferta(models.Model):
    perfil = models.ForeignKey(Perfil, related_name='none+')
    oferta = models.ForeignKey(Oferta, related_name='none+')

    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'VisitaAOferta'


class VisitaAPerfil(models.Model):
    perfil = models.ForeignKey(Perfil, related_name='none+')
    perfil_visitado = models.ForeignKey(Perfil, related_name='none+')

    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'VisitaAPerfil'



