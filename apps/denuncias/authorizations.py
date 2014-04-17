from core.authorization import es_admin, es_perfil_denunciante
from core.modelo import resolver_usuario
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class DenunciaAuth(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        # El administrador puede ver cualquier denuncia. Un denunciante puede ver solo las que ha emitido
        if es_admin(bundle.request.user):
            return object_list
        else:
            return object_list.filter(denunciante__usuario=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return es_admin(bundle.request.user) or resolver_usuario(bundle.obj.denunciante) == bundle.request.user

    def create_list(self, object_list, bundle):
        # Solo los perfiles denunciantes pueden crear denuncias
        if es_perfil_denunciante(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def create_detail(self, object_list, bundle):
        return es_perfil_denunciante(bundle.request.user)

    def update_detail(self, object_list, bundle):
        # Solo los administradores pueden modificar denuncias (para cambiar el estado)
        return es_admin(bundle.request.user)
