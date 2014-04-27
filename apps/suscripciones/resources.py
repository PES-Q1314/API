# coding=utf-8
from apps.suscripciones.authorizations import SuscripcionAuth
from apps.suscripciones.models import Suscripcion
from apps.usuarios.models import Perfil
from core.accion import action, response, ActionResourceMixin
from core.autorizacion import es_perfil_suscriptor
from core.http import HttpOK
from core.recurso import MetaGenerica
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

    def delete_detail(self, request, **kwargs):
        try:
            super().delete_detail(request, **kwargs)
        except Suscripcion.YaValorada:
            raise ImmediateHttpResponse(HttpBadRequest())


class RecursoSuscribible(ActionResourceMixin, ModelResource):
    estado_de_la_suscripcion = fields.CharField(readonly=True, use_in='detail')
    suscripciones = fields.ToManyField(SuscripcionResource, 'suscripciones', full=True, null=True)

    # TODO: Devolver el estado de la suscripcion o 'no suscrito'.
    def dehydrate_estado_de_la_suscripcion(self, bundle):
        return 'aa'

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

