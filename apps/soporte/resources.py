from apps.soporte.authorizations import SoporteAuth
from apps.soporte.models import EntradaFAQ, DocumentoDeSoporte
from core.resource import MetaGenerica
from tastypie.resources import ModelResource


class EntradaFAQResource(ModelResource):
    Meta = MetaGenerica(modelo=EntradaFAQ)
    Meta.authorization = SoporteAuth()


class DocumentoDeSoporteResource(ModelResource):
    Meta = MetaGenerica(modelo=DocumentoDeSoporte)
    Meta.authorization = SoporteAuth()
