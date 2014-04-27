# coding=utf-8
from apps.base.models import Idioma, ConocimientoTecnico, SectorDelMercado, Departamento, Especialidad
from core.recurso import MetaGenerica
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource


class IdiomaResource(ModelResource):
    Meta = MetaGenerica(modelo=Idioma)
    Meta.allowed_methods = ['get']


class ConocimientoTecnicoResource(ModelResource):
    Meta = MetaGenerica(modelo=ConocimientoTecnico)
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get']
    Meta.authorization = Authorization()


class SectorDelMercadoResource(ModelResource):
    Meta = MetaGenerica(modelo=SectorDelMercado)
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get']
    Meta.authorization = Authorization()


class DepartamentoResource(ModelResource):
    Meta = MetaGenerica(modelo=Departamento)
    Meta.allowed_methods = ['get']


class EspecialidadResource(ModelResource):
    Meta = MetaGenerica(modelo=Especialidad)
    Meta.allowed_methods = ['get']