from api import settings
from django.db import models


class Estudiante(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='estudiante')

