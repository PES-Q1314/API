# coding=utf-8
from apps.base.resources import ConocimientoTecnicoResource, SectorDelMercadoResource, IdiomaResource
from apps.congelaciones.resources import RecursoCongelable
from apps.usuarios.models import Estudiante, Profesor, Empresa, EstudianteTieneConocimientoTecnico, \
    EstudianteTieneExperienciaLaboral, EstudianteHablaIdioma
from core.resource import MetaGenerica
from tastypie import fields
from tastypie.resources import ModelResource


class EstudianteTieneConocimientoTecnicoResource(ModelResource):
    conocimiento = fields.ForeignKey(ConocimientoTecnicoResource, 'conocimiento', full=True)
    Meta = MetaGenerica(modelo=EstudianteTieneConocimientoTecnico)


class EstudianteTieneExperienciaLaboralResource(ModelResource):
    sector = fields.ForeignKey(SectorDelMercadoResource, 'sector', full=True)
    Meta = MetaGenerica(modelo=EstudianteTieneExperienciaLaboral)


class EstudianteHablaIdiomaResource(ModelResource):
    idioma = fields.ForeignKey(IdiomaResource, 'idioma', full=True)
    Meta = MetaGenerica(modelo=EstudianteHablaIdioma)


class EstudianteResource(RecursoCongelable, ModelResource):
    conocimientos_tecnicos = fields.ToManyField(EstudianteTieneConocimientoTecnicoResource,
                                                'conocimiento_tecnico_set', full=True)
    experiencia_laboral = fields.ToManyField(EstudianteTieneExperienciaLaboralResource,
                                             'experiencia_laboral_set', full=True)
    idiomas = fields.ToManyField(EstudianteHablaIdiomaResource, 'idioma_set', full=True)

    Meta = MetaGenerica(modelo=Estudiante)
    Meta.list_allowed_methods = ['get']
    Meta.detail_allowed_methods = ['get', 'patch']


class ProfesorResource(RecursoCongelable, ModelResource):
    Meta = MetaGenerica(modelo=Profesor)
    Meta.list_allowed_methods = ['get']
    Meta.detail_allowed_methods = ['get', 'patch']


class EmpresaResource(RecursoCongelable, ModelResource):
    Meta = MetaGenerica(modelo=Empresa)
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'put', 'patch', 'delete']