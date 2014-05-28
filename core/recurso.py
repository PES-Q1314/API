from core.autenticacion import SystemAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.exceptions import Unauthorized
from tastypie.resources import ModelResource


def get_model_fields(model):
    return model._meta.fields


def get_complete_filtering(model):
    return {f.name: ALL_WITH_RELATIONS for f in get_model_fields(model)}


def get_complete_ordering(model):
    return [f.name for f in get_model_fields(model)]



class RecursoGenerico(ModelResource):
    def get_schema(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        bundle = self.build_bundle(request=request)
        self.authorized_schema(bundle)
        return self.create_response(request, self.build_schema())

    def authorized_schema(self, bundle):
        auth_result = False
        try:
            auth_result = self._meta.authorization.schema(bundle)
            if not auth_result is True:
                raise Unauthorized()
        except Unauthorized as e:
            self.unauthorized_result(e)
        return auth_result

class MetaGenerica:
    def __init__(self, modelo):
        self.modelo = modelo
        self.queryset = modelo.objects.all()
        self.authorization = ReadOnlyAuthorization()
        self.authentication = SystemAuthentication()
        self.filtering = get_complete_filtering(modelo)
        self.ordering = get_complete_ordering(modelo)
        self.always_return_data = True