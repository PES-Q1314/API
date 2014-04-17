from apps.base.models import Idioma, ConocimientoTecnico
from apps.congelaciones.models import Congelacion
from apps.cuentas.models import SystemUser
from apps.ofertas.factory import DATOS_OBLIGATORIOS_OFERTA
from apps.ofertas.models import OfertaDeEmpresa
from apps.soporte.factory import crear_documento
from apps.usuarios.factory import crear_administrador, crear_empresa
from core.modelo import resolver_usuario
from tastypie.test import ResourceTestCase


class SoporteResourcesTest(ResourceTestCase):
    def setUp(self):
        super().setUp()

        self.creds = [{'username': '{0}'.format(i), 'password': '1234'} for i in range(2)]
        self.users = [
            SystemUser.objects.create_user(c['username'], '{0}@{0}.upc.edu'.format(c['username']), c['password']) for c
            in self.creds]

        self.admin = crear_administrador(self.users[0])
        self.empr = crear_empresa(self.users[1])
        self.doc = crear_documento()

    def login(self, credentials=None):
        if credentials is None:
            credentials = self.creds[0]
        self.assertHttpOK(self.api_client.post('/api/systemuser/login/', data=credentials))

    def test_get(self):
        self.login(self.creds[0])  # Como admin podemos ver el documento
        self.assertHttpOK(self.api_client.get('/api/documentodesoporte/{0}'.format(self.doc.pk)))

        self.login(self.creds[1])  # Como empresa también
        self.assertHttpOK(self.api_client.get('/api/documentodesoporte/{0}'.format(self.doc.pk)))

    def test_edit(self):
        self.login(self.creds[0])  # Como admin podemos crear/modificar/borrar documentos
        d = {'titulo': 'Titulo nuevo'}
        self.assertHttpAccepted(self.api_client.patch('/api/documentodesoporte/{0}'.format(self.doc.pk), data=d))

        self.login(self.creds[1])  # Como empresa no
        self.assertHttpUnauthorized(self.api_client.delete('/api/documentodesoporte/{0}'.format(self.doc.pk)))