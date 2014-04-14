# coding=utf-8
from apps.congelaciones.models import Congelacion
from apps.suscripciones.models import Suscripcion
from core.resource import get_model_fields, MetaGenerica
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource


class CongelacionResource(ModelResource):
    Meta = MetaGenerica(modelo=Congelacion)


class RecursoCongelable(ModelResource):
    congelaciones = fields.ToManyField(CongelacionResource, 'congelaciones', full=True)
    modificado_tras_una_congelacion = fields.BooleanField()

    def dehydrate_modificado_tras_una_congelacion(self, bundle):
        return bundle.obj.ha_sido_modificado_tras_una_congelacion