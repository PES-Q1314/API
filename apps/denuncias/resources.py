from apps.denuncias.authorizations import DenunciaAuth
from apps.denuncias.models import Denuncia, PerfilDenunciante
from apps.usuarios.models import Perfil
from core.accion import ActionResourceMixin, action, response
from core.autorizacion import es_perfil_denunciante, es_admin
from core.http import HttpOK
from core.recurso import MetaGenerica
from django.core.exceptions import ObjectDoesNotExist
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpUnauthorized
from tastypie.resources import ModelResource


class DenunciaResource(ModelResource):
    Meta = MetaGenerica(modelo=Denuncia)
    Meta.authorization = DenunciaAuth()


class RecursoDenunciable(ActionResourceMixin, ModelResource):
    denuncias = fields.ToManyField(DenunciaResource, 'denuncias', full=True, null=True)

    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Elemento denunciado correctamente")
    @response(HttpBadRequest, "No es posible denunciar el elemento")
    def denunciar(self, request, motivo):
        if not es_perfil_denunciante(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            denunciante = Perfil.objects.get_subclass(usuario=request.user)
            Denuncia.objects.create(modelo=modelo, denunciante=denunciante, motivo=motivo)
            return self.create_response(request, {}, HttpOK)
        except Exception:
            raise ImmediateHttpResponse(HttpBadRequest())

    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Denuncias descartadas")
    @response(HttpBadRequest, "No es posible descartar las denuncias")
    def descartar_denuncias(self, request):
        if not es_admin(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            modelo.denuncias.filter(estado='pendiente').update(estado='desestimada')
            return self.create_response(request, {}, HttpOK)
        except Exception:
            raise ImmediateHttpResponse(HttpBadRequest())