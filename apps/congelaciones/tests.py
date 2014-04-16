from apps.base.models import Idioma, ConocimientoTecnico
from apps.congelaciones.models import Congelacion
from apps.cuentas.models import SystemUser
from apps.ofertas.factory import DATOS_OBLIGATORIOS_OFERTA
from apps.ofertas.models import OfertaDeEmpresa
from apps.usuarios.factory import crear_administrador, crear_empresa
from tastypie.test import ResourceTestCase


class CongelacionesResourcesTest(ResourceTestCase):

    def setUp(self):
        super().setUp()

        self.creds = [{'username': '{0}'.format(i), 'password': '1234'} for i in range(3)]
        self.users = [
            SystemUser.objects.create_user(c['username'], '{0}@{0}.upc.edu'.format(c['username']), c['password']) for c
            in self.creds]

        self.admin = crear_administrador(self.users[0])
        self.empr = crear_empresa(self.users[1])

        d = DATOS_OBLIGATORIOS_OFERTA
        d['usuario'] = self.empr
        self.of = OfertaDeEmpresa.objects.create(**d)

    def login(self, credentials=None):
        if credentials is None:
            credentials = self.creds[0]
        self.assertHttpOK(self.api_client.post('/api/systemuser/login/', data=credentials))

    def test_congelar(self):
        before = Congelacion.objects.count()
        self.login(self.creds[1]) # Nos autenticamos como empresa
        d = {'motivo': '...'}
        self.assertHttpUnauthorized(self.api_client.post('/api/ofertadeempresa/{0}/congelar'.format(self.of.pk), data=d))

        self.login(self.creds[0]) # Nos autenticamos como administrador
        self.assertHttpOK(self.api_client.post('/api/ofertadeempresa/{0}/congelar'.format(self.of.pk), data=d))
        self.assertGreater(Congelacion.objects.count(), before)

    def test_descongelar(self):
        c = Congelacion.objects.create(modelo=self.of, motivo='...')
        before = Congelacion.objects.filter(estado='pendiente').count()
        self.login(self.creds[0]) # Nos autenticamos como administrador
        self.assertHttpOK(self.api_client.post('/api/ofertadeempresa/{0}/descongelar'.format(self.of.pk), data={}))
        self.assertLess(Congelacion.objects.filter(estado='pendiente').count(), before)

    def test_get(self):
        c = Congelacion.objects.create(modelo=self.of, motivo='...')
        self.login(self.creds[0]) # Como admin podemos ver la congelación
        self.assertHttpOK(self.api_client.get('/api/congelacion/{0}'.format(c.pk)))

        self.login(self.creds[1]) # Como empresa también
        self.assertHttpOK(self.api_client.get('/api/congelacion/{0}'.format(c.pk)))

        self.login(self.creds[2]) # Como otro usuario cualquiera, no
        self.assertHttpUnauthorized(self.api_client.get('/api/congelacion/{0}'.format(c.pk)))