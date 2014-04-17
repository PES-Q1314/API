# coding=utf-8
from apps.analitica.authorizations import AnaliticaGeneralAuth, AnaliticaPremiumAuth
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.resources import Resource


class AnaliticaGeneralResource(Resource):
    # Placeholder. Procesaría y devolvería todas las estadísticas de la información general del sistema

    class Meta:
        authorization = AnaliticaGeneralAuth()
        authentication = SessionAuthentication()


class AnaliticaPremiumResource(Resource):
    # Placeholder. Procesaría y devolvería todas las estadísticas de la información general del sistema

    class Meta:
        authorization = AnaliticaPremiumAuth()
        authentication = SessionAuthentication()



