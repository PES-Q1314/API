# coding=utf-8
from apps.congelaciones.authorizations import CongelacionAuth
from apps.congelaciones.models import Congelacion
from apps.usuarios.models import Perfil, Administrador
from core.action import ActionResourceMixin, action, response
from core.authorization import es_admin
from core.http import HttpOK
from core.modelo import resolver_usuario
from core.resource import MetaGenerica
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpUnauthorized
from tastypie.resources import ModelResource




class CongelacionResource(ModelResource):
    Meta = MetaGenerica(modelo=Congelacion)
    Meta.authorization = CongelacionAuth()


class RecursoCongelable(ActionResourceMixin, ModelResource):
    congelaciones = fields.ToManyField(CongelacionResource, 'congelaciones', full=True, null=True)
    modificado_tras_una_congelacion = fields.BooleanField()

    def dehydrate_modificado_tras_una_congelacion(self, bundle):
        return bundle.obj.ha_sido_modificado_tras_una_congelacion

    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Elemento congelado correctamente")
    @response(HttpBadRequest, "No es posible congelar el elemento")
    def congelar(self, request, motivo):
        if not es_admin(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            Congelacion.objects.create(modelo=modelo, motivo=motivo)
            return self.create_response(request, {}, HttpOK)
        except Exception:
            raise ImmediateHttpResponse(HttpBadRequest())

    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Elemento descongelado correctamente")
    @response(HttpBadRequest, "No es posible descongelar el elemento")
    def descongelar(self, request):
        if not es_admin(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            modelo.congelaciones.filter(estado='pendiente').update(estado='resuelta')
            return self.create_response(request, {}, HttpOK)
        except Exception:
            raise ImmediateHttpResponse(HttpBadRequest())


    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Elemento eliminado correctamente")
    @response(HttpBadRequest, "No es posible eliminar el elemento")
    def eliminar(self, request, motivo):
        if not es_admin(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())
        try:
            # Para que los elementos eliminados no interfieran con el sistema, creamos
            # una copia serializada de los mismos y los guardamos en un fichero de eliminaciones
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            modelo.delete()
            return self.create_response(request, {}, HttpOK)
        except Exception:
            raise ImmediateHttpResponse(HttpBadRequest())



