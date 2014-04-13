# coding=utf-8
from apps.suscripciones.models import Suscripcion
from core.autorizaciones import AutorizacionDeAutor
from core.resource import get_model_fields
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource


class SuscripcionResource(ModelResource):

    class Meta:
        queryset = Suscripcion.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()

        filtering = {f: ALL_WITH_RELATIONS for f in get_model_fields(Suscripcion)}
        ordering = [f for f in get_model_fields(Suscripcion)]

    def obj_create(self, bundle, **kwargs):
        return super(SuscripcionResource, self).obj_create(bundle, autor=bundle.request.user.perfil)


class RecursoSuscribible(ModelResource):
    suscripciones = fields.ToManyField(SuscripcionResource, 'suscripciones', null=True)