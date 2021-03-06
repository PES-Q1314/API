from apps.lista_negra.authorizations import ListaNegraAuth
from apps.lista_negra.models import ElementoDeLaListaNegra
from core.accion import ActionResourceMixin, action, response
from core.autorizacion import es_admin
from core.http import HttpOK
from core.recurso import MetaGenerica, RecursoGenerico
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpUnauthorized


class ElementoDeLaListaNegraResource(RecursoGenerico):
    Meta = MetaGenerica(modelo=ElementoDeLaListaNegra)
    Meta.authorization = ListaNegraAuth()


class RecursoIncluibleEnLaListaNegra(ActionResourceMixin, RecursoGenerico):

    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Elemento añadido a la lista negra")
    @response(HttpBadRequest, "No es posible añadir el elemento a la lista negra")
    def meter_en_la_lista_negra(self, request, motivo):
        if not es_admin(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            ElementoDeLaListaNegra.objects.create(modelo=modelo, motivo=motivo)
            return self.create_response(request, {}, HttpOK)
        except Exception:
            raise ImmediateHttpResponse(HttpBadRequest())

    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Elemento quitado de la lista negra")
    @response(HttpBadRequest, "No es posible quitar el elemento de la lista negra")
    def quitar_de_la_lista_negra(self, request, motivo):
        if not es_admin(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            modelo.entrada_en_la_lista_negra.all().delete()
            return self.create_response(request, {}, HttpOK)
        except Exception:
            raise ImmediateHttpResponse(HttpBadRequest())