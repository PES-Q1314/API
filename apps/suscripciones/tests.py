from apps.base.models import Idioma, ConocimientoTecnico
from apps.congelaciones.models import Congelacion
from apps.cuentas.models import SystemUser
from apps.denuncias.models import Denuncia
from apps.ofertas.factory import DATOS_OBLIGATORIOS_OFERTA
from apps.ofertas.models import OfertaDeEmpresa
from apps.suscripciones.models import Suscripcion
from apps.usuarios.factory import crear_administrador, crear_empresa, crear_estudiante
from tastypie.test import ResourceTestCase


class SuscripcionesResourcesTest(ResourceTestCase):
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

    def test_suscribirse(self):
        before = Suscripcion.objects.count()
        self.login(self.creds[0])  # Nos autenticamos como administrador (no es perfil suscriptor)
        self.assertHttpUnauthorized(
            self.api_client.post('/api/ofertadeempresa/{0}/suscribirse'.format(self.of.pk), data={}))

        self.login(self.creds[1])  # Nos autenticamos como estudiante (pefil suscriptor)
        self.assertHttpOK(self.api_client.post('/api/ofertadeempresa/{0}/suscribirse'.format(self.of.pk), data={}))
        self.assertGreater(Suscripcion.objects.count(), before)

    def test_get(self):
        d = Suscripcion.objects.create(modelo=self.of, suscriptor=self.est)
        self.login(self.creds[0])  # Como admin no podemos ver la suscripcion
        self.assertHttpUnauthorized(self.api_client.get('/api/suscripcion/{0}'.format(d.pk)))

        self.login(self.creds[1])  # Como estudiante suscriptor sí
        self.assertHttpOK(self.api_client.get('/api/suscripcion/{0}'.format(d.pk)))

        self.login(self.creds[2])  # Como empresa que crea la oferta también
        self.assertHttpOK(self.api_client.get('/api/suscripcion/{0}'.format(d.pk)))

    def test_delete(self):
        d = Suscripcion.objects.create(modelo=self.of, suscriptor=self.est, estado='aceptada')
        self.login(self.creds[0])  # Como admin no podemos borrarla
        self.assertHttpUnauthorized(self.api_client.delete('/api/suscripcion/{0}'.format(d.pk)))

        self.login(self.creds[1])  # Como estudiante suscriptor sí, pero si su estado no es 'pendiente', no
        self.assertHttpBadRequest(self.api_client.delete('/api/suscripcion/{0}'.format(d.pk)))

        d.estado = 'pendiente'
        d.save()
        self.assertHttpAccepted(self.api_client.delete('/api/suscripcion/{0}'.format(d.pk)))