from apps.denuncias.models import Denuncia
from apps.usuarios.models import Perfil
from core.action import ActionResourceMixin, action, response
from core.http import HttpOK
from core.resource import MetaGenerica
from django.core.exceptions import ObjectDoesNotExist
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource


class DenunciaResource(ModelResource):
    Meta = MetaGenerica(modelo=Denuncia)


class RecursoDenunciable(ActionResourceMixin, ModelResource):
    denuncias = fields.ToManyField(DenunciaResource, 'denuncias', full=True)

    @action(allowed=('post',), static=False)
    @response(HttpOK, "Elemento denunciado correctamente")
    @response(HttpBadRequest, "No es posible denunciar el elemento")
    def denunciar(self, request):
        try:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            denunciante = Perfil.objects.get_subclass(usuario__id=request.user.id)
            Denuncia.objects.create(modelo=modelo, denunciante=denunciante, motivo='...')
            return self.create_response(request, {}, HttpOK)
        # TODO: quitarlo cuando haya autenticación obligatoria
        except ObjectDoesNotExist:
            modelo = self._meta.object_class.objects.get(pk=request.api['pk'])
            denunciante = Perfil.objects.all().select_subclasses().first()
            Denuncia.objects.create(modelo=modelo, denunciante=denunciante, motivo='...')
            return self.create_response(request, {}, HttpOK)
        except Exception as e:
            raise ImmediateHttpResponse(HttpBadRequest())