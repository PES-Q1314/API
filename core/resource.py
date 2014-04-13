from tastypie.authentication import SessionAuthentication
from tastypie.constants import ALL_WITH_RELATIONS


def get_model_fields(model):
    return model._meta.fields


class MetaGenerica(object):
    MODELO = None
    queryset = MODELO.objects.all()
    authentication = SessionAuthentication()
    filtering = {f: ALL_WITH_RELATIONS for f in get_model_fields(MODELO)}
    ordering = [f for f in get_model_fields(MODELO)]