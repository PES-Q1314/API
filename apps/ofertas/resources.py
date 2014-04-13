from apps.base.resources import ConocimientoTecnicoResource, IdiomaResource, SectorDelMercadoResource, \
    EspecialidadResource
from apps.congelaciones.resources import RecursoCongelable
from apps.ofertas.models import OfertaDeEmpresa, Oferta
from apps.suscripciones.resources import RecursoSuscribible
from core.autorizaciones import AutorizacionDeAutor
from core.resource import get_model_fields
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource



class OfertaResource(RecursoCongelable, RecursoSuscribible, ModelResource):
    especialidades = fields.ToManyField(EspecialidadResource, 'especialidades', full=True)
    requisitos_de_conocimiento_tecnico = fields.ToManyField(ConocimientoTecnicoResource,
                                                            'requisitos_de_conocimiento_tecnico', full=True)
    requisitos_de_experiencia_laboral = fields.ToManyField(SectorDelMercadoResource,
                                                           'requisitos_de_experiencia_laboral', full=True)
    requisitos_de_idioma = fields.ToManyField(IdiomaResource, 'requisitos_de_idioma', full=True)

    class Meta:
        queryset = Oferta.objects.all()
        authentication = SessionAuthentication()
        authorization = AutorizacionDeAutor()

        filtering = {f: ALL_WITH_RELATIONS for f in get_model_fields(Oferta)}
        ordering = [f for f in get_model_fields(Oferta)]

    def obj_create(self, bundle, **kwargs):
        return super(OfertaResource, self).obj_create(bundle, autor=bundle.request.user.perfil)

