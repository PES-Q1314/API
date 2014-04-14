from apps.lista_negra.models import ElementoDeLaListaNegra
from core.action import ActionResourceMixin, action, response
from core.http import HttpOK
from core.resource import MetaGenerica
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource


class ElementoDeLaListaNegraResource(ModelResource):
    Meta = MetaGenerica(modelo=ElementoDeLaListaNegra)


class RecursoIncluibleEnLaListaNegra(ActionResourceMixin, ModelResource):
    pass

    @action(allowed=('post',), static=False)
    @response(HttpOK, "Elemento añadido a la lista negra")
    @response(HttpBadRequest, "No es posible añadir el elemento a la lista negra")
    def meter_en_la_lista_negra(self, request):
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            ElementoDeLaListaNegra.objects.create(modelo=modelo, motivo='...')
            return self.create_response(request, {}, HttpOK)
        except Exception:
            raise ImmediateHttpResponse(HttpBadRequest())