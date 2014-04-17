from apps.base.models import Idioma, ConocimientoTecnico
from apps.congelaciones.models import Congelacion
from apps.cuentas.models import SystemUser
from apps.denuncias.models import Denuncia
from apps.lista_negra.models import ElementoDeLaListaNegra
from apps.ofertas.factory import DATOS_OBLIGATORIOS_OFERTA
from apps.ofertas.models import OfertaDeEmpresa
from apps.usuarios.factory import crear_administrador, crear_empresa, crear_estudiante
from tastypie.test import ResourceTestCase


class ListaNegraResourcesTest(ResourceTestCase):
    def setUp(self):
        super().setUp()

        self.creds = [{'username': '{0}'.format(i), 'password': '1234'} for i in range(3)]
        self.users = [
            SystemUser.objects.create_user(c['username'], '{0}@{0}.upc.edu'.format(c['username']), c['password']) for c
            in self.creds]

        self.admin = crear_administrador(self.users[0])
        self.empr = crear_empresa(self.users[1])


    def login(self, credentials=None):
        if credentials is None:
            credentials = self.creds[0]
        self.assertHttpOK(self.api_client.post('/api/systemuser/login/', data=credentials))

    def test_anyadir_a_la_lista(self):
        before = ElementoDeLaListaNegra.objects.count()
        self.login(self.creds[1])  # Nos autenticamos como empresa (no podemos tocar la lista negra)
        d = {'motivo': '...'}
        self.assertHttpUnauthorized(
            self.api_client.post('/api/empresa/{0}/meter_en_la_lista_negra/'.format(self.empr.pk), data=d))

        self.login(self.creds[0])  # Nos autenticamos como administrador
        self.assertHttpOK(
            self.api_client.post('/api/empresa/{0}/meter_en_la_lista_negra/'.format(self.empr.pk), data=d))
        self.assertGreater(ElementoDeLaListaNegra.objects.count(), before)

    def test_get(self):
        e = ElementoDeLaListaNegra.objects.create(modelo=self.empr, motivo='...')
        self.login(self.creds[0])  # Como admin podemos ver la lista negra
        self.assertHttpOK(self.api_client.get('/api/elementodelalistanegra/{0}'.format(e.pk)))

        self.login(self.creds[1])  # Como empresa no
        self.assertHttpUnauthorized(self.api_client.get('/api/elementodelalistanegra/{0}'.format(e.pk)))