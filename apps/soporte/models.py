import os
from django.db import models


def get_file_path(instance, filename):
    return os.path.join('documento', filename)


class EntradaFAQ(models.Model):
    pregunta = models.CharField(max_length=200, unique=True)
    respuesta = models.TextField(max_length=5000)

    class Meta:
        db_table = 'EntradaFAQ'


class DocumentoDeSoporte(models.Model):
    titulo = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=500)
    documento = models.FileField(upload_to=get_file_path)

    class Meta:
        db_table = 'DocumentoDeSoporte'