from apps.base.models import Idioma, ConocimientoTecnico
from apps.cuentas.models import SystemUser
from tastypie.test import ResourceTestCase


class BaseResourcesTest(ResourceTestCase):

    def setUp(self):
        super().setUp()

        self.creds = [{'username': '{0}'.format(i), 'password': '1234'} for i in range(3)]
        self.users = [
            SystemUser.objects.create_user(c['username'], '{0}@{0}.upc.edu'.format(c['username']), c['password']) for c
            in self.creds]

    def login(self, credentials=None):
        if credentials is None:
            credentials = self.creds[0]
        self.assertHttpOK(self.api_client.post('/api/systemuser/login/', data=credentials))

    def test_get(self):
        self.login()
        resp = self.api_client.get('/api/idioma/')
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], Idioma.objects.count())

    def test_post_unauthorized(self):
        self.login()
        idioma = {'codigo':'zz', 'idioma': 'Zizarauense'}
        self.assertHttpMethodNotAllowed(self.api_client.post('/api/idioma/', data=idioma))

    def test_post_authorized(self):
        self.login()
        conocimiento_tecnico = {'conocimiento': 'AJAX'}
        self.assertHttpCreated(self.api_client.post('/api/conocimientotecnico/', data=conocimiento_tecnico))
        self.assertTrue(ConocimientoTecnico.objects.filter(conocimiento='AJAX').exists())