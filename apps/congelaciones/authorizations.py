from core.autorizacion import es_admin
from core.modelo import resolver_usuario
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class CongelacionAuth(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        # Un administrador puede ver todas las congelaciones; Un usuario solo las que le afectan
        if es_admin(bundle.request.user):
            return object_list
        else:
            allowed = []
            for obj in object_list:
                if (resolver_usuario(bundle.obj.modelo) == bundle.request.user):
                    allowed.append(obj)
            return allowed

    def read_detail(self, object_list, bundle):
        return es_admin(bundle.request.user) or (resolver_usuario(bundle.obj.modelo) == bundle.request.user)


    def create_list(self, object_list, bundle):
        # Solo los administradores pueden crear congelaciones
        if es_admin(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def create_detail(self, object_list, bundle):
        return es_admin(bundle.request.user)

    def update_detail(self, object_list, bundle):
        # Solo los administradores pueden modificar el estado de las congelaciones
        return es_admin(bundle.request.user)

