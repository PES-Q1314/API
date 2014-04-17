from core.authorization import es_admin, es_perfil_denunciante, es_perfil_suscriptor
from django.db.models import Q
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class SuscripcionAuth(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        # Una suscripción pueden verla los suscriptores y los autores del modelo al que está asociada la suscripción
        return object_list.filter(
            Q(suscriptor__usuario=bundle.request.user) | Q(modelo__usuario__usuario=bundle.request.user))

    def read_detail(self, object_list, bundle):
        return bundle.request.user in (bundle.obj.suscriptor.usuario, bundle.obj.modelo.usuario.usuario)

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
        return bundle.obj.modelo.usuario.usuario == bundle.request.user

    def delete_detail(self, object_list, bundle):
        # Una suscripción solo puede ser eliminada por su autor
        return bundle.obj.suscriptor.usuario == bundle.request.user
