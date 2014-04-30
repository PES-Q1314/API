from apps.base import enums
from apps.base.factory import crear_sector, crear_conocimiento
from apps.base.models import ConocimientoTecnico
from apps.cuentas.models import SystemUser
from apps.usuarios.factory import crear_estudiante, crear_profesor, crear_empresa, crear_administrador
from apps.usuarios.models import Estudiante, EstudianteTieneConocimientoTecnico, Empresa
from tastypie.test import ResourceTestCase


class UsuariosResourcesTest(ResourceTestCase):
    def setUp(self):
        super().setUp()

        self.creds = [{'username': 'test{0}'.format(i), 'password': '1234'} for i in range(6)]
        self.users = [
            SystemUser.objects.create_user(c['username'], '{0}@{0}.upc.edu'.format(c['username']), c['password']) for c
            in self.creds]

        # 0 es un estudiante, 1 es un profesor, 2 es una empresa, y 3 es una empresa premium
        self.est = crear_estudiante(self.users[0])
        self.prof = crear_profesor(self.users[1])
        self.empr = crear_empresa(self.users[2])
        self.prem = crear_empresa(self.users[3], es_premium=True)
        self.admin = crear_administrador(self.users[5])

    def login(self, credentials=None):
        if credentials is None:
            credentials = self.creds[0]
        self.assertHttpOK(self.api_client.post('/api/systemuser/login/', data=credentials))

    def test_get_closed_profile(self):
        # Un estudiante puede consultar cualquier perfil cerrado
        self.login(self.creds[0])
        self.assertHttpOK(self.api_client.get('/api/estudiante/'))

        # Una empresa no-premium, sin embargo, no
        self.login(self.creds[2])
        self.assertHttpUnauthorized(self.api_client.get('/api/estudiante/'))

    def test_get_open_profile(self):
        # Incluso las empresas no-premium pueden ver un perfil abierto
        self.login(self.creds[2])
        self.assertHttpOK(self.api_client.get('/api/empresa/'))

    def test_patch_profile(self):
        # No puedes modificar un perfil que no sea el tuyo
        self.login(self.creds[1])
        d = {'dni': '45532212X'}
        self.assertHttpUnauthorized(self.api_client.patch('/api/estudiante/{0}'.format(self.est.pk), data=d))

        self.login(self.creds[0])
        self.assertHttpAccepted(self.api_client.patch('/api/estudiante/{0}'.format(self.est.pk), data=d))

    def test_post_delete_open_profile(self):
        # Este usuario no tiene perfil (podrá crear un perfil abierto, véase registrarse como empresa)
        self.login(self.creds[4])
        d = {'nombre': 'testEmpresa', 'cif': '24234325X'}
        self.assertHttpCreated(self.api_client.post('/api/empresa/', data=d))

    def test_post_conocimiento(self):
        # Como estudiante, queremos añadir un conocimiento a nuestra lista de ellos
        self.login(self.creds[0])
        c = ConocimientoTecnico.objects.first() if ConocimientoTecnico.objects.exists() else crear_conocimiento()
        d = {'conocimiento': '/api/conocimientotecnico/{0}'.format(c.pk)}
        self.assertHttpCreated(self.api_client.post('/api/estudiantetieneconocimientotecnico/', data=d))

        # Si lo intenta hacer un profesor, no le estará permitido
        self.login(self.creds[1])
        self.assertHttpUnauthorized(self.api_client.post('/api/estudiantetieneconocimientotecnico/', data=d))

    def test_delete_conocimiento(self):
        crear_estudiante(self.users[4])
        # En este punto, hay al menos dos estudiantes, cada uno con conocimientos técnicos
        self.login(self.creds[0])
        self.assertTrue(self.est.conocimiento_tecnico_set.all().exists())
        self.assertHttpAccepted(self.api_client.delete('/api/estudiantetieneconocimientotecnico/'))
        self.assertFalse(self.est.conocimiento_tecnico_set.all().exists())
        # Borramos nuestros propios conocimientos, pero no los de los demás
        self.assertTrue(EstudianteTieneConocimientoTecnico.objects.exists())

    def test_verificar_premium(self):
        self.login(self.creds[2])
        d = {'clave_del_servicio_externo': 13445}
        self.assertHttpOK(self.api_client.post('/api/empresa/{0}/verificar_premium/'.format(self.empr.pk), data=d))

    def test_aceptar_empresa(self):
        self.empr.esta_activa = False  # A priori la empresa no está activa
        self.empr.save()

        self.login(self.creds[0])  # Un estudiante no puede aceptar la empresa
        self.assertHttpUnauthorized(self.api_client.post('/api/empresa/{0}/aceptar/'.format(self.empr.pk), data={}))

        self.login(self.creds[5])  # Un administrador sí
        self.assertFalse(Empresa.objects.get(id=self.empr.id).esta_activa)
        self.assertHttpOK(self.api_client.post('/api/empresa/{0}/aceptar/'.format(self.empr.pk), data={}))
        self.assertTrue(Empresa.objects.get(id=self.empr.id).esta_activa)


    def test_rechazar_empresa(self):
        self.empr.esta_activa = False  # A priori la empresa no está activa
        self.empr.save()

        self.login(self.creds[0])  # Un estudiante no puede rechazar la empresa
        self.assertHttpUnauthorized(self.api_client.post('/api/empresa/{0}/rechazar/'.format(self.empr.pk), data={}))

        self.login(self.creds[5])  # Un administrador sí
        self.assertFalse(Empresa.objects.get(id=self.empr.id).esta_activa)
        self.assertHttpOK(self.api_client.post('/api/empresa/{0}/rechazar/'.format(self.empr.pk), data={}))
        self.assertFalse(Empresa.objects.filter(id=self.empr.id).exists())








