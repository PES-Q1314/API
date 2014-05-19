from apps.base.factory import crear_sector
from apps.base.models import SectorDelMercado
from apps.cuentas.models import SystemUser
from apps.ofertas.factory import DATOS_OBLIGATORIOS_OFERTA, crear_oferta_de_departamento, crear_oferta_de_empresa, \
    crear_oferta_de_proyecto_emprendedor
from apps.ofertas.models import OfertaDeProyectoEmprendedor, Oferta, OfertaDeEmpresa
from apps.usuarios.factory import crear_estudiante, crear_profesor, crear_empresa
from tastypie.test import ResourceTestCase


class OfertasResourcesTest(ResourceTestCase):
    def setUp(self):
        super().setUp()

        self.creds = [{'username': 'test{0}'.format(i), 'password': '1234'} for i in range(3)]
        self.users = [
            SystemUser.objects.create_user(c['username'], '{0}@{0}.upc.edu'.format(c['username']), c['password']) for c
            in self.creds]

        # 0 es un estudiante, 1 es un profesor, 2 es una empresa, y 3 es una empresa premium
        self.est = crear_estudiante(self.users[0])
        self.prof = crear_profesor(self.users[1])
        self.empr = crear_empresa(self.users[2])

    def login(self, credentials=None):
        if credentials is None:
            credentials = self.creds[0]
        self.assertHttpOK(self.api_client.post('/api/systemuser/login/', data=credentials))

    def test_get_oferta(self):
        # Cualquiera (autenticado) puede consultar una oferta
        self.login(self.creds[0])
        self.assertHttpOK(self.api_client.get('/api/ofertadeempresa/'))
        self.assertHttpOK(self.api_client.get('/api/ofertadedepartamento/'))
        resp = self.api_client.get('/api/ofertadeproyectoemprendedor/')
        self.assertHttpOK(resp)
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], OfertaDeProyectoEmprendedor.objects.count())

    def test_post_requisito_experiencia(self):
        # Queremos añadir a la oferta un requisito de experiencia
        self.login(self.creds[0])
        d = DATOS_OBLIGATORIOS_OFERTA
        d['usuario'] = self.est
        of = OfertaDeProyectoEmprendedor.objects.create(**d)
        s = SectorDelMercado.objects.first() if SectorDelMercado.objects.exists() else crear_sector()
        d = {
            'oferta': '/api/oferta/{0}'.format(of.pk),
            'sector': '/api/sectordelmercado/{0}'.format(s.pk),
            'meses': 3
        }
        self.assertHttpCreated(self.api_client.post('/api/requisitodeexperiencialaboral/', data=d))

        # Si lo intenta hacer un profesor, no le estará permitido
        self.login(self.creds[1])
        self.assertHttpUnauthorized(self.api_client.post('/api/requisitodeexperiencialaboral/', data=d))

    def test_get_beneficios_laborales(self):
        # Comprobamos que los obtenemos correctamente
        of = crear_oferta_de_empresa(u=self.empr, extras=False)
        self.login(self.creds[2])
        self.assertIsNotNone(of.beneficios_laborales)
        resp = self.api_client.get('/api/ofertadeempresa/{0}/'.format(of.pk))
        self.assertHttpOK(resp)
        before = self.deserialize(resp)['beneficios_laborales']['transporte']

        # Comprobamos que los modificamos correctamente (desde el recurso específico)
        d = {'transporte': not before}
        self.assertHttpAccepted(
            self.api_client.patch(('/api/beneficioslaborales/{0}'.format(of.beneficios_laborales.pk)), data=d))
        self.assertEqual(OfertaDeEmpresa.objects.get(pk=of.pk).beneficios_laborales.transporte, d['transporte'])

