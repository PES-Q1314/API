from tastypie.authentication import SessionAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS


def get_model_fields(model):
    return model._meta.fields


def get_complete_filtering(model):
    return {f.name: ALL_WITH_RELATIONS for f in get_model_fields(model)}


def get_complete_ordering(model):
    return [f.name for f in get_model_fields(model)]



class MetaGenerica:
    def __init__(self, modelo):
        self.modelo = modelo
        self.queryset = modelo.objects.all()
        self.authorization = Authorization()
        self.authentication = Authentication()
        self.filtering = get_complete_filtering(modelo)
        self.ordering = get_complete_ordering(modelo)