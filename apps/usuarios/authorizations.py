from core.autorizacion import es_empresa_no_premium, es_estudiante, ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class OpenProfileAuth(ReadOnlyAuthorization):
    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return True

    def update_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.usuario == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.usuario == bundle.request.user

    def delete_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.usuario == bundle.request.user:
                allowed.append(obj)
        return allowed

    def delete_detail(self, object_list, bundle):
        return bundle.obj.usuario == bundle.request.user


class ClosedProfileAuth(ReadOnlyAuthorization):

    def read_list(self, object_list, bundle):
        # Todos tienen acceso al perfil menos las empresas sin cuenta premium
        return object_list

    def read_detail(self, object_list, bundle):
        return True

    def update_list(self, object_list, bundle):
        allowed = []
        for obj in object_list:
            if obj.usuario == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.usuario == bundle.request.user


class EstudiantePlusAuth(ClosedProfileAuth):

    def create_list(self, object_list, bundle):
        if es_estudiante(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def create_detail(self, object_list, bundle):
        return es_estudiante(bundle.request.user)

    def update_list(self, object_list, bundle):
        raise Unauthorized()

    def update_detail(self, object_list, bundle):
        raise Unauthorized()

    def delete_list(self, object_list, bundle):
        if es_estudiante(bundle.request.user):
            allowed = []
            for obj in object_list:
                if obj.estudiante.usuario == bundle.request.user:
                    allowed.append(obj)
            return allowed
        else:
            raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        return es_estudiante(bundle.request.user) and bundle.obj.estudiante.usuario == bundle.request.user
