from apps.base.resources import ConocimientoTecnicoResource, IdiomaResource, SectorDelMercadoResource, \
    EspecialidadResource
from apps.congelaciones.resources import RecursoCongelable
from apps.denuncias.resources import RecursoDenunciable
from apps.ofertas.authorizations import OfertaAuth, OfertaPlusAuth, BeneficiosLaboralesAuth
from apps.ofertas.models import OfertaDeEmpresa, RequisitoDeConocimientoTecnico, RequisitoDeExperienciaLaboral, \
    RequisitoDeIdioma, OfertaDeProyectoEmprendedor, OfertaDeDepartamento, Oferta, BeneficiosLaborales
from apps.suscripciones.resources import RecursoSuscribible
from apps.usuarios.models import Perfil
from apps.usuarios.resources import EmpresaResource, ProfesorResource, EstudianteResource
from core.recurso import MetaGenerica, RecursoGenerico
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpUnauthorized


class OfertaResource(RecursoDenunciable, RecursoCongelable, RecursoSuscribible, RecursoGenerico):
    tipo = fields.CharField(readonly=True)
    beneficios_laborales = fields.OneToOneField('apps.ofertas.resources.BeneficiosLaboralesResource',
                                                'beneficios_laborales', full=True, null=True, readonly=True)
    especialidades = fields.ToManyField(EspecialidadResource, 'especialidades', full=True, null=True)

    requisitos_de_conocimiento_tecnico = fields.ToManyField(
        'apps.ofertas.resources.RequisitoDeConocimientoTecnicoResource',
        'requisito_de_conocimiento_tecnico_set', full=True, null=True)
    requisitos_de_experiencia_laboral = fields.ToManyField(
        'apps.ofertas.resources.RequisitoDeExperienciaLaboralResource',
        'requisito_de_experiencia_laboral_set', full=True, null=True)
    requisitos_de_idioma = fields.ToManyField('apps.ofertas.resources.RequisitoDeIdiomaResource',
                                              'requisito_de_idioma_set',
                                              full=True, null=True)

    Meta = MetaGenerica(modelo=Oferta)
    Meta.authorization = OfertaAuth()

    def dehydrate_tipo(self, bundle):
        try:
            return Oferta.objects.get_subclass(pk=bundle.obj.pk).__class__.__name__
        except:
            return 'Ninguno'

    def obj_create(self, bundle, **kwargs):
        try:
            p = Perfil.objects.get_subclass(usuario=bundle.request.user)
            return super().obj_create(bundle, usuario=p)
        except Exception as e:
            raise ImmediateHttpResponse(HttpUnauthorized())


class BeneficiosLaboralesResource(RecursoGenerico):
    Meta = MetaGenerica(modelo=BeneficiosLaborales)
    Meta.authorization = BeneficiosLaboralesAuth()


class OfertaDeEmpresaResource(OfertaResource):
    usuario = fields.ForeignKey(EmpresaResource, 'usuario')
    Meta = MetaGenerica(modelo=OfertaDeEmpresa)
    Meta.authorization = OfertaAuth()


class OfertaDeDepartamentoResource(OfertaResource):
    usuario = fields.ForeignKey(ProfesorResource, 'usuario')
    Meta = MetaGenerica(modelo=OfertaDeDepartamento)
    Meta.authorization = OfertaAuth()


class OfertaDeProyectoEmprendedorResource(OfertaResource):
    usuario = fields.ForeignKey(EstudianteResource, 'usuario')
    Meta = MetaGenerica(modelo=OfertaDeProyectoEmprendedor)
    Meta.authorization = OfertaAuth()


##################
# RELACIONES M2M #
##################

class RequisitoPlusMixin(RecursoGenerico):
    oferta = fields.ForeignKey(OfertaResource, 'oferta')


class RequisitoDeConocimientoTecnicoResource(RequisitoPlusMixin, RecursoGenerico):
    conocimiento = fields.ForeignKey(ConocimientoTecnicoResource, 'conocimiento', full=True)
    Meta = MetaGenerica(modelo=RequisitoDeConocimientoTecnico)
    Meta.authorization = OfertaPlusAuth()


class RequisitoDeExperienciaLaboralResource(RequisitoPlusMixin, RecursoGenerico):
    sector = fields.ForeignKey(SectorDelMercadoResource, 'sector', full=True)
    Meta = MetaGenerica(modelo=RequisitoDeExperienciaLaboral)
    Meta.authorization = OfertaPlusAuth()


class RequisitoDeIdiomaResource(RequisitoPlusMixin, RecursoGenerico):
    idioma = fields.ForeignKey(IdiomaResource, 'idioma', full=True)
    Meta = MetaGenerica(modelo=RequisitoDeIdioma)
    Meta.authorization = OfertaPlusAuth()