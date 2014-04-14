# coding=utf-8
from apps.suscripciones.models import Suscripcion
from core.action import action, response
from core.autorizaciones import AutorizacionDeAutor
from core.http import HttpOK
from core.resource import get_model_fields, MetaGenerica
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource


class SuscripcionResource(ModelResource):
    Meta = MetaGenerica(modelo=Suscripcion)

    def obj_create(self, bundle, **kwargs):
        return super(SuscripcionResource, self).obj_create(bundle, autor=bundle.request.user.perfil)


class RecursoSuscribible(ModelResource):
    suscripciones = fields.ToManyField(SuscripcionResource, 'suscripciones', full=True)

