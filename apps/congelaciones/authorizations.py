from apps.usuarios.models import Perfil, Administrador
from core.authorization import es_admin
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class CongelacionAuth(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        if es_admin(bundle):
            return object_list
        else:
            return object_list.filter(modelo__usuario=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return es_admin(bundle) or bundle.obj.modelo.usuario == bundle.request.user

    def create_list(self, object_list, bundle):
        if es_admin(bundle):
            return object_list
        else:
            raise Unauthorized()

    def create_detail(self, object_list, bundle):
        return es_admin(bundle)

    def update_detail(self, object_list, bundle):
        return es_admin(bundle)

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
