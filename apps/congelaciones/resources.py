# coding=utf-8
from apps.congelaciones.models import Congelacion
from apps.suscripciones.models import Suscripcion
from core.resource import get_model_fields
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource


class CongelacionResource(ModelResource):
    class Meta:
        queryset = Congelacion.objects.all()
        authentication = SessionAuthentication()
        authorization = Authorization()

        filtering = {f: ALL_WITH_RELATIONS for f in get_model_fields(Congelacion)}
        ordering = [f for f in get_model_fields(Congelacion)]


class RecursoCongelable(ModelResource):
    congelaciones = fields.ToManyField(CongelacionResource, 'congelaciones', null=True)
    modificado_tras_una_congelacion = fields.BooleanField()

    def dehydrate_modificado_tras_una_congelacion(self, bundle):
        return bundle.obj.ha_sido_modificado_tras_una_congelacion