from core.autorizacion import es_perfil_suscriptor, ReadOnlyAuthorization
from core.modelo import resolver_usuario
from tastypie.exceptions import Unauthorized


class SuscripcionAuth(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        # Una suscripción pueden verla los suscriptores y los autores del modelo al que está asociada la suscripción
        allowed = []
        for obj in object_list:
            if bundle.request.user in (resolver_usuario(obj.suscriptor), resolver_usuario(obj.modelo)):
                allowed.append(obj)
        return allowed

    def read_detail(self, object_list, bundle):
        return bundle.request.user in (resolver_usuario(bundle.obj.suscriptor), resolver_usuario(bundle.obj.modelo))

    def create_list(self, object_list, bundle):
        # Una suscripción pueden crearla solo los suscriptores
        if es_perfil_suscriptor(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def create_detail(self, object_list, bundle):
        return es_perfil_suscriptor(bundle.request.user)

    def update_detail(self, object_list, bundle):
        # Una suscripción pueden actualizarla (cambiar el estado)
        # los autores del modelo al que está asociada la suscripción
        return resolver_usuario(bundle.obj.modelo) == bundle.request.user
