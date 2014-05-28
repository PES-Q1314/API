from apps.ofertas.models import Oferta
from core.autorizacion import es_admin, ReadOnlyAuthorization


class OfertaAuth(ReadOnlyAuthorization):
    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return True

    def update_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.usuario.usuario == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.usuario.usuario == bundle.request.user

    def delete_list(self, object_list, bundle):
        return object_list if es_admin(bundle.request.user) else []

    def delete_detail(self, object_list, bundle):
        return es_admin(bundle.request.user)


def get_usuario(oferta):
    return Oferta.objects.get_subclass(id=oferta.id).usuario.usuario


class BeneficiosLaboralesAuth(ReadOnlyAuthorization):
    def update_detail(self, object_list, bundle):
        return get_usuario(bundle.obj.oferta) == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if get_usuario(obj.oferta) == bundle.request.user:
                allowed.append(obj)
        return allowed


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
