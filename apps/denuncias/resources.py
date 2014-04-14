from apps.denuncias.models import Denuncia
from core.resource import MetaGenerica
from tastypie import fields
from tastypie.resources import ModelResource


class DenunciaResource(ModelResource):
    Meta = MetaGenerica(modelo=Denuncia)


class RecursoDenunciable(ModelResource):
    denuncias = fields.ToManyField(DenunciaResource, 'denuncias', full=True)