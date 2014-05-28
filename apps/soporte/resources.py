from apps.soporte.authorizations import SoporteAuth
from apps.soporte.models import EntradaFAQ, DocumentoDeSoporte
from core.recurso import MetaGenerica, RecursoGenerico


class EntradaFAQResource(RecursoGenerico):
    Meta = MetaGenerica(modelo=EntradaFAQ)
    Meta.authorization = SoporteAuth()


class DocumentoDeSoporteResource(RecursoGenerico):
    Meta = MetaGenerica(modelo=DocumentoDeSoporte)
    Meta.authorization = SoporteAuth()
