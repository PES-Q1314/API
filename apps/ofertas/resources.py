from apps.base.resources import ConocimientoTecnicoResource, IdiomaResource, SectorDelMercadoResource
from apps.ofertas.models import OfertaDeEmpresa, Oferta
from apps.suscripciones.resources import RecursoSuscribible
from core.autorizaciones import AutorizacionDeAutor
from core.resource import get_model_fields
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource





class OfertaResource(RecursoSuscribible, ModelResource):
    requisitos_de_conocimiento_tecnico = fields.ToManyField(ConocimientoTecnicoResource,
                                                            'requisitos_de_conocimiento_tecnico', full=True)
    requisitos_de_experiencia_laboral = fields.ToManyField(SectorDelMercadoResource,
                                                           'requisitos_de_experiencia_laboral', full=True)
    requisitos_de_idioma = fields.ToManyField(IdiomaResource, 'requisitos_de_idioma', full=True)

    class Meta:
        queryset = OfertaDeEmpresa.objects.all()
        authentication = SessionAuthentication()
        authorization = AutorizacionDeAutor()

        filtering = {f: ALL_WITH_RELATIONS for f in get_model_fields(Oferta)}
        ordering = [f for f in get_model_fields(Oferta)]

    def obj_create(self, bundle, **kwargs):
        return super(OfertaResource, self).obj_create(bundle, autor=bundle.request.user.perfil)

