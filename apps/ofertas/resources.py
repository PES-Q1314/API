from apps.base.resources import ConocimientoTecnicoResource, IdiomaResource, SectorDelMercadoResource, \
    EspecialidadResource
from apps.congelaciones.resources import RecursoCongelable
from apps.ofertas.models import OfertaDeEmpresa, Oferta, RequisitoDeConocimientoTecnico, RequisitoDeExperienciaLaboral, \
    RequisitoDeIdioma, OfertaDeProyectoEmprendedor, OfertaDeDepartamento
from apps.suscripciones.resources import RecursoSuscribible
from core.autorizaciones import AutorizacionDeAutor
from core.resource import get_model_fields, MetaGenerica
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource


class RequisitoDeConocimientoTecnicoResource(ModelResource):
    conocimiento = fields.ForeignKey(ConocimientoTecnicoResource, 'conocimiento', full=True)
    Meta = MetaGenerica(modelo=RequisitoDeConocimientoTecnico)


class RequisitoDeExperienciaLaboralResource(ModelResource):
    sector = fields.ForeignKey(SectorDelMercadoResource, 'sector', full=True)
    Meta = MetaGenerica(modelo=RequisitoDeExperienciaLaboral)


class RequisitoDeIdiomaResource(ModelResource):
    idioma = fields.ForeignKey(IdiomaResource, 'idioma', full=True)
    Meta = MetaGenerica(modelo=RequisitoDeIdioma)


class RecursoOfertaGenerica(RecursoCongelable, RecursoSuscribible, ModelResource):
    especialidades = fields.ToManyField(EspecialidadResource, 'especialidades', full=True)
    requisitos_de_conocimiento_tecnico = fields.ToManyField(RequisitoDeConocimientoTecnicoResource,
                                                            'requisito_de_conocimiento_tecnico_set', full=True)
    requisitos_de_experiencia_laboral = fields.ToManyField(RequisitoDeExperienciaLaboralResource,
                                                           'requisito_de_experiencia_laboral_set', full=True)
    requisitos_de_idioma = fields.ToManyField(RequisitoDeIdiomaResource, 'requisito_de_idioma_set', full=True)


class OfertaDeEmpresaResource(RecursoOfertaGenerica):
    Meta = MetaGenerica(modelo=OfertaDeEmpresa)


class OfertaDeDepartamentoResource(RecursoOfertaGenerica):
    Meta = MetaGenerica(modelo=OfertaDeDepartamento)


class OfertaDeProyectoEmprendedorResource(RecursoOfertaGenerica):
    Meta = MetaGenerica(modelo=OfertaDeProyectoEmprendedor)


