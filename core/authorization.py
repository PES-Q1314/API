from apps.denuncias.models import PerfilDenunciante
from apps.suscripciones.models import PerfilSuscriptor
from apps.usuarios.models import Estudiante, Empresa, Profesor, Administrador, Perfil


def es_empresa(u):
        return Empresa.objects.filter(usuario=u).exists()


def es_empresa_no_premium(u):
        e = Empresa.objects.filter(usuario=u)
        return e.exists() and not e.first().es_premium


def es_estudiante(u):
        return Estudiante.objects.filter(usuario=u).exists()


def es_profesor(u):
        return Profesor.objects.filter(usuario=u).exists()


def es_admin(u):
    return Administrador.objects.filter(usuario=u).exists()


def es_perfil_denunciante(u):
    return issubclass(Perfil.objects.get_subclass(usuario=u).__class__, PerfilDenunciante)


def es_perfil_suscritor(u):
    return issubclass(Perfil.objects.get_subclass(usuario=u).__class__, PerfilSuscriptor)