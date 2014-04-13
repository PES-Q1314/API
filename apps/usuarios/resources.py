# coding=utf-8
from apps.base.resources import ConocimientoTecnicoResource, SectorDelMercadoResource, IdiomaResource
from apps.congelaciones.resources import RecursoCongelable
from apps.usuarios.models import Estudiante, Profesor, Empresa
from core.autorizaciones import AutorizacionDePerfil
from core.resource import get_model_fields
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource


class MetaGenerica(object):
    MODELO = None
    queryset = MODELO.objects.all()
    authentication = SessionAuthentication()
    filtering = {f: ALL_WITH_RELATIONS for f in get_model_fields(MODELO)}
    ordering = [f for f in get_model_fields(MODELO)]


class EstudianteResource(RecursoCongelable, ModelResource):
    conocimientos_tecnicos = fields.ToManyField(ConocimientoTecnicoResource,
                                                'conocimientos_tecnicos', full=True)
    experiencia_laboral = fields.ToManyField(SectorDelMercadoResource,
                                             'experiencia_laboral', full=True)
    idiomas = fields.ToManyField(IdiomaResource, 'idiomas', full=True)


    class Meta:
        queryset = Estudiante.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'patch']
        authentication = SessionAuthentication()
        authorization = AutorizacionDePerfil()

        # TODO: Abstraer el filtrado y ordenado, así como authentication y authorization a una clase Meta genérica
        filtering = {f: ALL_WITH_RELATIONS for f in get_model_fields(Estudiante)}
        ordering = [f for f in get_model_fields(Estudiante)]


class ProfesorResource(RecursoCongelable, ModelResource):
    class Meta:
        queryset = Profesor.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'patch']
        authentication = SessionAuthentication()
        authorization = AutorizacionDePerfil()

        filtering = {f: ALL_WITH_RELATIONS for f in get_model_fields(Profesor)}
        ordering = [f for f in get_model_fields(Profesor)]


class EmpresaResource(RecursoCongelable, ModelResource):
    class Meta:
        queryset = Empresa.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put', 'patch', 'delete']
        authentication = SessionAuthentication()
        authorization = AutorizacionDePerfil()

        filtering = {f: ALL_WITH_RELATIONS for f in get_model_fields(Empresa)}
        ordering = [f for f in get_model_fields(Empresa)]