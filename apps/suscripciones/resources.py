# coding=utf-8
from apps.suscripciones.authorizations import SuscripcionAuth
from apps.suscripciones.models import Suscripcion
from apps.usuarios.models import Perfil
from core.accion import action, response, ActionResourceMixin
from core.autorizacion import es_perfil_suscriptor
from core.http import HttpOK
from core.recurso import MetaGenerica, RecursoGenerico
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpUnauthorized


class SuscripcionResource(RecursoGenerico):
    Meta = MetaGenerica(modelo=Suscripcion)
    Meta.authorization = SuscripcionAuth()

    def dehydrate(self, bundle):
        bundle.data['oferta'] = {
            'titulo': bundle.obj.modelo.titulo,
            'fecha': bundle.obj.modelo.fecha_de_creacion,
            'usuario': bundle.obj.modelo.usuario.nombre if hasattr(bundle.obj.modelo, 'usuario') else ''
        }
        return bundle

    def obj_create(self, bundle, **kwargs):
        return super(SuscripcionResource, self).obj_create(bundle, usuario=bundle.request.user.perfil)

    def delete_detail(self, request, **kwargs):
        try:
            super().delete_detail(request, **kwargs)
        except Suscripcion.YaValorada:
            raise ImmediateHttpResponse(HttpBadRequest())


class RecursoSuscribible(ActionResourceMixin, RecursoGenerico):
    estado_de_la_suscripcion = fields.CharField(readonly=True, use_in='detail')
    suscripciones = fields.ToManyField(SuscripcionResource, 'suscripciones', full=True, null=True)

    def dehydrate_estado_de_la_suscripcion(self, bundle):
        s = bundle.obj.suscripcion_del_usuario(Perfil.objects.get_subclass(usuario=bundle.request.user))
        return s.estado if s is not None else 'no suscrito'


    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Suscrito correctamente al elemento")
    @response(HttpUnauthorized, "No está autorizado para realizar esta acción")
    @response(HttpBadRequest, "No es posible suscribirse al elemento")
    def suscribirse(self, request, **kwargs):
        if not es_perfil_suscriptor(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            suscriptor = Perfil.objects.get_subclass(usuario=request.user)
            Suscripcion.objects.create(modelo=modelo, suscriptor=suscriptor)
            return self.create_response(request, {}, HttpOK)
        except Exception as e:
            raise ImmediateHttpResponse(HttpBadRequest())


    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "La suscripcion al elemento ha sido eliminada correctamente")
    @response(HttpBadRequest, "No es posible eliminar esta suscripcion")
    def dessuscribirse(self, request, **kwargs):
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            modelo.suscripcion_del_usuario(Perfil.objects.get_subclass(usuario=request.user)).delete()
            return self.create_response(request, {}, HttpOK)
        except Exception:
            raise ImmediateHttpResponse(HttpBadRequest())