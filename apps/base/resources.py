# coding=utf-8
from apps.base.models import Idioma, ConocimientoTecnico, SectorDelMercado, Departamento, Especialidad
from core.recurso import MetaGenerica, RecursoGenerico
from tastypie.authorization import Authorization


class IdiomaResource(RecursoGenerico):
    Meta = MetaGenerica(modelo=Idioma)
    Meta.allowed_methods = ['get']


class ConocimientoTecnicoResource(RecursoGenerico):
    Meta = MetaGenerica(modelo=ConocimientoTecnico)
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get']
    Meta.authorization = Authorization()


class SectorDelMercadoResource(RecursoGenerico):
    Meta = MetaGenerica(modelo=SectorDelMercado)
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get']
    Meta.authorization = Authorization()


class DepartamentoResource(RecursoGenerico):
    Meta = MetaGenerica(modelo=Departamento)
    Meta.allowed_methods = ['get']


class EspecialidadResource(RecursoGenerico):
    Meta = MetaGenerica(modelo=Especialidad)
    Meta.allowed_methods = ['get']