from apps.cuentas.models import SystemUser
from tastypie.test import ResourceTestCase


class BaseResourcesTest(ResourceTestCase):

    def setUp(self):
        super().setUp()

        self.creds = [{
            'username': '{0}'.format(i),
            'email': '{0}@{0}.upc.edu'.format(i),
            'password': '1234'
        } for i in range(3)]
        self.users = [SystemUser.objects.create_user(**c) for c in self.creds]

    def login(self, credentials):
        self.assertHttpOK(self.api_client.post('/api/login/', data=credentials))

    def test_x(self):
        pass