from apps.base.resources import ConocimientoTecnicoResource, IdiomaResource, SectorDelMercadoResource, \
    EspecialidadResource
from apps.congelaciones.resources import RecursoCongelable
from apps.denuncias.resources import RecursoDenunciable
from apps.ofertas.authorizations import OfertaAuth, OfertaPlusAuth
from apps.ofertas.models import OfertaDeEmpresa, RequisitoDeConocimientoTecnico, RequisitoDeExperienciaLaboral, \
    RequisitoDeIdioma, OfertaDeProyectoEmprendedor, OfertaDeDepartamento, Oferta
from apps.suscripciones.resources import RecursoSuscribible
from apps.usuarios.models import Perfil, Estudiante
from apps.usuarios.resources import EmpresaResource, ProfesorResource, EstudianteResource
from core.resource import MetaGenerica
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource


class OfertaResource(RecursoDenunciable, RecursoCongelable, RecursoSuscribible, ModelResource):
    especialidades = fields.ToManyField(EspecialidadResource, 'especialidades', full=True, null=True)

    requisitos_de_conocimiento_tecnico = fields.ToManyField(
        'apps.ofertas.resources.RequisitoDeConocimientoTecnicoResource',
        'requisito_de_conocimiento_tecnico_set', full=True, null=True)
    requisitos_de_experiencia_laboral = fields.ToManyField('apps.ofertas.resources.RequisitoDeExperienciaLaboralResource',
                                                           'requisito_de_experiencia_laboral_set', full=True, null=True)
    requisitos_de_idioma = fields.ToManyField('apps.ofertas.resources.RequisitoDeIdiomaResource', 'requisito_de_idioma_set',
                                              full=True, null=True)

    Meta = MetaGenerica(modelo=Oferta)
    Meta.authorization = OfertaAuth()


    def obj_create(self, bundle, **kwargs):
        try:
            p = Perfil.objects.get_subclass(usuario=bundle.request.user)
            return super().obj_create(bundle, autor=p)
        except Exception as e:
            raise ImmediateHttpResponse(HttpUnauthorized())



class OfertaDeEmpresaResource(OfertaResource):
    autor = fields.ForeignKey(EmpresaResource, 'autor')
    Meta = MetaGenerica(modelo=OfertaDeEmpresa)
    Meta.authorization = OfertaAuth()



class OfertaDeDepartamentoResource(OfertaResource):
    autor = fields.ForeignKey(ProfesorResource, 'autor')
    Meta = MetaGenerica(modelo=OfertaDeDepartamento)
    Meta.authorization = OfertaAuth()


class OfertaDeProyectoEmprendedorResource(OfertaResource):
    autor = fields.ForeignKey(EstudianteResource, 'autor')
    Meta = MetaGenerica(modelo=OfertaDeProyectoEmprendedor)
    Meta.authorization = OfertaAuth()



##################
# RELACIONES M2M #
##################

class RequisitoPlusMixin(ModelResource):
    oferta = fields.ForeignKey(OfertaResource, 'oferta')

class RequisitoDeConocimientoTecnicoResource(RequisitoPlusMixin, ModelResource):
    conocimiento = fields.ForeignKey(ConocimientoTecnicoResource, 'conocimiento', full=True)
    Meta = MetaGenerica(modelo=RequisitoDeConocimientoTecnico)
    Meta.authorization = OfertaPlusAuth()


class RequisitoDeExperienciaLaboralResource(RequisitoPlusMixin, ModelResource):
    sector = fields.ForeignKey(SectorDelMercadoResource, 'sector', full=True)
    Meta = MetaGenerica(modelo=RequisitoDeExperienciaLaboral)
    Meta.authorization = OfertaPlusAuth()


class RequisitoDeIdiomaResource(RequisitoPlusMixin, ModelResource):
    idioma = fields.ForeignKey(IdiomaResource, 'idioma', full=True)
    Meta = MetaGenerica(modelo=RequisitoDeIdioma)
    Meta.authorization = OfertaPlusAuth()