from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ModeloIncluibleEnLaListaNegra(models.Model):
    entrada_en_la_lista_negra = GenericRelation('ElementoDeLaListaNegra')

    class Meta:
        abstract = True

    @property
    def esta_en_la_lista_negra(self):
        return self.entrada_en_la_lista_negra.all().exists()


class ElementoDeLaListaNegra(models.Model):
    # Apuntador genérico a Modelos Incluibles en la Lista Negra
    content_type = models.ForeignKey(ContentType, related_name='none+')
    object_id = models.PositiveIntegerField()
    modelo = GenericForeignKey()

    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=500)

    class Meta:
        # The Generic FK is really a Generic OneToOne relationship
        unique_together = ('content_type', 'object_id')
        db_table = 'ElementoDeLaListaNegra'

