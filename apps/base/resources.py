# coding=utf-8
from apps.base.models import Idioma, ConocimientoTecnico, SectorDelMercado, Departamento
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource


class IdiomaResource(ModelResource):

    class Meta:
        queryset = Idioma.objects.all()

        # Hay un conjunto fijo de idiomas, y solo se puede consultar
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = Authorization()

        filtering = {
            'codigo': ALL,
            'idioma': ALL
        }

        ordering = ['codigo', 'idioma']


class ConocimientoTecnicoResource(ModelResource):

    class Meta:
        queryset = ConocimientoTecnico.objects.all()

        # No puede borrarse un conocimiento ya introducido. Todos pueden consultarse libremente
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = Authorization()

        filtering = {
            'conocimiento': ALL
        }

        ordering = ['conocimiento']


class SectorDelMercadoResource(ModelResource):

    class Meta:
        queryset = SectorDelMercado.objects.all()

        # No puede borrarse un sector ya introducido. Todos pueden consultarse libremente
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = Authorization()

        filtering = {
            'sector': ALL
        }

        ordering = ['sector']


class DepartamentoResource(ModelResource):

    class Meta:
        queryset = Departamento.objects.all()

        # Hay un conjunto fijo de departamentos, y solo se puede consultar
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = Authorization()

        filtering = {
            'siglas': ALL,
            'nombre': ALL
        }

        ordering = ['siglas', 'nombre']