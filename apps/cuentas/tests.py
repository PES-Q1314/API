from apps.cuentas.models import SystemUser
from tastypie.test import ResourceTestCase


class BaseResourcesTest(ResourceTestCase):
    def setUp(self):
        super().setUp()

        self.creds = [{'username': '{0}'.format(i), 'password': '1234'} for i in range(3)]
        self.users = [
            SystemUser.objects.create_user(c['username'], '{0}@{0}.upc.edu'.format(c['username']), c['password']) for c
            in self.creds]

    def login(self, credentials):
        self.assertHttpOK(self.api_client.post('/api/systemuser/login/', data=credentials))

    def test_login_process(self):
        # El usuario no está logueado
        self.assertHttpUnauthorized(self.api_client.get('/api/systemuser/logincheck'))
        # El usuario se autentica
        self.login(self.creds[0])
        # El usuario está logueado
        self.assertHttpOK(self.api_client.get('/api/systemuser/logincheck'))
        # El usuario se des-loguea
        self.assertHttpOK(self.api_client.post('/api/systemuser/logout'))
        # El usuario no está logueado
        self.assertHttpUnauthorized(self.api_client.get('/api/systemuser/logincheck'))

    def test_register(self):
        # Registramos un nuevo usuario de manera correcta
        new_user = {'username': 'example.test', 'email': 'example@test.com', 'password': '1234'}
        self.assertHttpCreated(self.api_client.post('/api/systemuser/register', data=new_user))
        # Tratamos de registrar un usuario con datos incompletos
        bad_user = {'username': 'example.test'}
        self.assertHttpBadRequest(self.api_client.post('/api/systemuser/register', data=bad_user))

