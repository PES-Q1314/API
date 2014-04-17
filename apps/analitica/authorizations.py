from core.authorization import es_admin, es_directivo, es_empresa_premium
from core.modelo import resolver_usuario
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.exceptions import Unauthorized


class AnaliticaGeneralAuth(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        # Un directivo es el único usuario capaz de ver los resultados de la analítica
        if es_directivo(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def read_detail(self, object_list, bundle):
        return es_directivo(bundle.request.user)


class AnaliticaPremiumAuth(ReadOnlyAuthorization):
    def read_list(self, object_list, bundle):
        # Un directivo es el único usuario capaz de ver los resultados de la analítica
        if es_empresa_premium(bundle.request.user):
            return object_list
        else:
            raise Unauthorized()

    def read_detail(self, object_list, bundle):
        return es_empresa_premium(bundle.request.user)

