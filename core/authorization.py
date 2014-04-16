from apps.usuarios.models import Estudiante, Empresa, Profesor, Administrador


def es_empresa(bundle):
        return Empresa.objects.filter(usuario=bundle.request.user).exists()


def es_empresa_no_premium(bundle):
        e = Empresa.objects.filter(usuario=bundle.request.user)
        return e.exists() and not e.first().es_premium


def es_estudiante(bundle):
        return Estudiante.objects.filter(usuario=bundle.request.user).exists()


def es_profesor(bundle):
        return Profesor.objects.filter(usuario=bundle.request.user).exists()


def es_admin(bundle):
    return Administrador.objects.filter(usuario=bundle.request.user).exists()