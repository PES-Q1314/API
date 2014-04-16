from apps.ofertas.models import Oferta
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class OfertaAuth(ReadOnlyAuthorization):
    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return True

    def update_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.autor.usuario == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.autor.usuario == bundle.request.user

    def delete_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.autor.usuario == bundle.request.user:
                allowed.append(obj)
        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.autor.usuario == bundle.request.user


def get_usuario(oferta):
    return Oferta.objects.get_subclass(id=oferta.id).autor.usuario

class OfertaPlusAuth(ReadOnlyAuthorization):
    def create_list(self, object_list, bundle):
        return self._list(object_list, bundle)

    def create_detail(self, object_list, bundle):
        return self._detail(object_list, bundle)

    def delete_detail(self, object_list, bundle):
        return self._detail(object_list, bundle)

    def _list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if get_usuario(obj.oferta) == bundle.request.user:
                allowed.append(obj)
        return allowed

    def _detail(self, object_list, bundle):
        return get_usuario(bundle.obj.oferta) == bundle.request.user
