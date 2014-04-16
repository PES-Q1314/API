from core.authorization import es_admin, es_perfil_denunciante
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class DenunciaAuth(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        if es_admin(bundle.request.user):
            return object_list
        else:
            return object_list.filter(denunciante__usuario=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return es_admin(bundle.request.user) or bundle.obj.denunciante.usuario == bundle.request.user

    def create_list(self, object_list, bundle):
        if es_perfil_denunciante(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def create_detail(self, object_list, bundle):
        return es_perfil_denunciante(bundle.request.user)

    def update_detail(self, object_list, bundle):
        return es_admin(bundle.request.user)

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
