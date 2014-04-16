# coding=utf-8
from apps.suscripciones.authorizations import SuscripcionAuth
from apps.suscripciones.models import Suscripcion
from apps.usuarios.models import Perfil
from core.action import action, response, ActionResourceMixin
from core.authorization import es_perfil_suscriptor
from core.http import HttpOK
from core.resource import MetaGenerica
from django.core.exceptions import ObjectDoesNotExist
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpUnauthorized
from tastypie.resources import ModelResource


class SuscripcionResource(ModelResource):
    Meta = MetaGenerica(modelo=Suscripcion)
    Meta.authorization = SuscripcionAuth()

    def obj_create(self, bundle, **kwargs):
        return super(SuscripcionResource, self).obj_create(bundle, autor=bundle.request.user.perfil)


class RecursoSuscribible(ActionResourceMixin, ModelResource):
    suscripciones = fields.ToManyField(SuscripcionResource, 'suscripciones', full=True, null=True)

    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Suscrito correctamente al elemento")
    @response(HttpBadRequest, "No es posible suscribirse al elemento")
    def suscribirse(self, request):
        if not es_perfil_suscriptor(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            suscriptor = Perfil.objects.get_subclass(usuario=request.user)
            Suscripcion.objects.create(modelo=modelo, suscriptor=suscriptor)
            return self.create_response(request, {}, HttpOK)
        except Exception as e:
            raise ImmediateHttpResponse(HttpBadRequest())

