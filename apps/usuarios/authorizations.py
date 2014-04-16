from apps.usuarios.models import Empresa, Estudiante
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


def es_empresa_no_premium(bundle):
        e = Empresa.objects.filter(usuario=bundle.request.user)
        return e.exists() and not e.first().es_premium


def es_estudiante(bundle):
        e = Estudiante.objects.filter(usuario=bundle.request.user)
        return e.exists()


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
        if es_empresa_no_premium(bundle):
            raise Unauthorized()
        else:
            return object_list

    def read_detail(self, object_list, bundle):
        return not es_empresa_no_premium(bundle)

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
        if es_estudiante(bundle):
            return object_list
        else:
            raise Unauthorized()

    def create_detail(self, object_list, bundle):
        return es_estudiante(bundle)

    def update_list(self, object_list, bundle):
        raise Unauthorized()

    def update_detail(self, object_list, bundle):
        raise Unauthorized()

    def delete_list(self, object_list, bundle):
        if es_estudiante(bundle):
            allowed = []
            for obj in object_list:
                if obj.estudiante.usuario == bundle.request.user:
                    allowed.append(obj)
            return allowed
        else:
            raise Unauthorized()

    def delete_detail(self, object_list, bundle):
        return es_estudiante(bundle) and bundle.obj.estudiante.usuario == bundle.request.user
