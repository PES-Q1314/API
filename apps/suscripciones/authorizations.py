from core.authorization import es_admin, es_perfil_denunciante, es_perfil_suscriptor
from core.modelo import resolver_usuario
from django.db.models import Q
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class SuscripcionAuth(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        # Una suscripción pueden verla los suscriptores y los autores del modelo al que está asociada la suscripción
        return object_list.filter(
            Q(suscriptor__usuario=bundle.request.user) | Q(modelo__usuario__usuario=bundle.request.user))

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

    def delete_detail(self, object_list, bundle):
        # Una suscripción solo puede ser eliminada por su autor
        return resolver_usuario(bundle.obj.suscriptor) == bundle.request.user
