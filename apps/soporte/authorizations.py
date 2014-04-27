from core.autorizacion import es_admin
from core.modelo import resolver_usuario
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class SoporteAuth(ReadOnlyAuthorization):
    # Cualquiera puede leer los documentos de soporte. Sin embargo,
    # solo los administradores pueden crearlos, modificarlos o borrarlos
    def create_list(self, object_list, bundle):
        return self._list(object_list, bundle)

    def create_detail(self, object_list, bundle):
        return self._detail(object_list, bundle)

    def update_list(self, object_list, bundle):
        return self._list(object_list, bundle)

    def update_detail(self, object_list, bundle):
        return self._detail(object_list, bundle)

    def delete_list(self, object_list, bundle):
        return self._list(object_list, bundle)

    def delete_detail(self, object_list, bundle):
        return self._detail(object_list, bundle)

    def _list(self, object_list, bundle):
        if es_admin(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def _detail(self, object_list, bundle):
        return es_admin(bundle.request.user)



