from apps.denuncias.models import PerfilDenunciante
from apps.suscripciones.models import PerfilSuscriptor
from apps.usuarios.models import Estudiante, Empresa, Profesor, Administrador, Perfil, Directivo
import tastypie


class ReadOnlyAuthorization(tastypie.authorization.ReadOnlyAuthorization):
    def schema(self, bundle):
        return True


def es_empresa(u):
    return Empresa.objects.filter(usuario=u).exists()


def es_empresa_premium(u):
    e = Empresa.objects.filter(usuario=u)
    return e.exists() and e.first().es_premium


def es_empresa_no_premium(u):
    e = Empresa.objects.filter(usuario=u)
    return e.exists() and not e.first().es_premium


def es_estudiante(u):
    return Estudiante.objects.filter(usuario=u).exists()


def es_profesor(u):
    return Profesor.objects.filter(usuario=u).exists()


def es_admin(u):
    return Administrador.objects.filter(usuario=u).exists()


def es_directivo(u):
    return Directivo.objects.filter(usuario=u).exists()


def es_perfil_denunciante(u):
    return issubclass(Perfil.objects.get_subclass(usuario=u).__class__, PerfilDenunciante)


def es_perfil_suscriptor(u):
    return issubclass(Perfil.objects.get_subclass(usuario=u).__class__, PerfilSuscriptor)