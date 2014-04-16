from core.authorization import es_admin, es_perfil_denunciante
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class ListaNegraAuth(ReadOnlyAuthorization):
    # Solo el administrador puede ver o manipular la lista negra
    def read_list(self, object_list, bundle):
        if es_admin(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def read_detail(self, object_list, bundle):
        return es_admin(bundle.request.user)

    def create_list(self, object_list, bundle):
        if es_admin(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def create_detail(self, object_list, bundle):
        return es_admin(bundle.request.user)

    def update_detail(self, object_list, bundle):
        return es_admin(bundle.request.user)

    def delete_list(self, object_list, bundle):
        if es_admin(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        return es_admin(bundle.request.user)
