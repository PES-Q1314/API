# coding=utf-8
from apps.suscripciones.models import Suscripcion
from apps.usuarios.models import Perfil
from core.action import action, response, ActionResourceMixin
from core.http import HttpOK
from core.resource import MetaGenerica
from django.core.exceptions import ObjectDoesNotExist
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource


class SuscripcionResource(ModelResource):
    Meta = MetaGenerica(modelo=Suscripcion)

    def obj_create(self, bundle, **kwargs):
        return super(SuscripcionResource, self).obj_create(bundle, autor=bundle.request.user.perfil)


class RecursoSuscribible(ActionResourceMixin, ModelResource):
    suscripciones = fields.ToManyField(SuscripcionResource, 'suscripciones', full=True, null=True)

    @action(allowed=('post',), static=False)
    @response(HttpOK, "Suscrito correctamente al elemento")
    @response(HttpBadRequest, "No es posible suscribirse al elemento")
    def suscribirse(self, request):
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            suscriptor = Perfil.objects.get_subclass(usuario__id=request.user.id)
            Suscripcion.objects.create(modelo=modelo, suscriptor=suscriptor, motivo='...')
            return self.create_response(request, {}, HttpOK)
        # TODO: quitarlo cuando haya autenticación obligatoria
        except ObjectDoesNotExist:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            suscriptor = Perfil.objects.all().select_subclasses().first()
            Suscripcion.objects.create(modelo=modelo, suscriptor=suscriptor, motivo='...')
            return self.create_response(request, {}, HttpOK)
        except Exception as e:
            raise ImmediateHttpResponse(HttpBadRequest())

