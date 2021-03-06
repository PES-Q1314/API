from apps.base.models import Idioma, ConocimientoTecnico
from apps.congelaciones.models import Congelacion
from apps.cuentas.models import SystemUser
from apps.denuncias.models import Denuncia
from apps.ofertas.factory import DATOS_OBLIGATORIOS_OFERTA
from apps.ofertas.models import OfertaDeEmpresa
from apps.usuarios.factory import crear_administrador, crear_empresa, crear_estudiante
from tastypie.test import ResourceTestCase


class DenunciasResourcesTest(ResourceTestCase):
    def setUp(self):
        super().setUp()

        self.creds = [{'username': '{0}'.format(i), 'password': '1234'} for i in range(3)]
        self.users = [
            SystemUser.objects.create_user(c['username'], '{0}@{0}.upc.edu'.format(c['username']), c['password']) for c
            in self.creds]

        self.admin = crear_administrador(self.users[0])
        self.est = crear_estudiante(self.users[1])
        self.empr = crear_empresa(self.users[2])

        d = DATOS_OBLIGATORIOS_OFERTA
        d['usuario'] = self.empr
        self.of = OfertaDeEmpresa.objects.create(**d)

    def login(self, credentials=None):
        if credentials is None:
            credentials = self.creds[0]
        self.assertHttpOK(self.api_client.post('/api/systemuser/login/', data=credentials))

    def test_denunciar(self):
        before = Denuncia.objects.count()
        self.login(self.creds[0])  # Nos autenticamos como administrador (no es perfil denunciante)
        d = {'motivo': '...'}
        self.assertHttpUnauthorized(
            self.api_client.post('/api/ofertadeempresa/{0}/denunciar'.format(self.of.pk), data=d))

        self.login(self.creds[1])  # Nos autenticamos como estudiante (pefil denunciante)
        self.assertHttpOK(self.api_client.post('/api/ofertadeempresa/{0}/denunciar'.format(self.of.pk), data=d))
        self.assertGreater(Denuncia.objects.count(), before)

    def test_descartar_denuncias(self):
        d = Denuncia.objects.create(modelo=self.of, denunciante=self.est, motivo='...')
        before = Denuncia.objects.filter(estado='pendiente').count()
        self.login(self.creds[0])  # Nos autenticamos como administrador
        self.assertHttpOK(self.api_client.post('/api/ofertadeempresa/{0}/descartar_denuncias'.format(self.of.pk), data={}))
        self.assertLess(Denuncia.objects.filter(estado='pendiente').count(), before)
        self.assertTrue(Denuncia.objects.filter(estado='desestimada').exists())

    def test_get(self):
        d = Denuncia.objects.create(modelo=self.of, denunciante=self.est, motivo='...')
        self.login(self.creds[0])  # Como admin podemos ver la denuncia
        self.assertHttpOK(self.api_client.get('/api/denuncia/{0}'.format(d.pk)))

        self.login(self.creds[1])  # Como estudiante también
        self.assertHttpOK(self.api_client.get('/api/denuncia/{0}'.format(d.pk)))

        self.login(self.creds[2])  # Como otro usuario cualquiera, no
        self.assertHttpUnauthorized(self.api_client.get('/api/denuncia/{0}'.format(d.pk)))