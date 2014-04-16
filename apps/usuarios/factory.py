from datetime import date
from apps.base import enums
from apps.base.factory import crear_especialidad, crear_departamento, crear_sector, crear_conocimiento, crear_idioma
from apps.base.models import Especialidad, ConocimientoTecnico, Idioma, SectorDelMercado, Departamento
from apps.usuarios.models import Estudiante, EstudianteTieneConocimientoTecnico, EstudianteHablaIdioma, \
    EstudianteTieneExperienciaLaboral, Profesor, Empresa


def crear_estudiante(u):
    datos = {
        'usuario': u,
        'nombre': u.username,
        'dni': str(u.id),
        'fecha_de_nacimiento': date(day=1, month=4, year=1990),
        'sexo': enums.SEXO[0][0],
        'telefono': str(u.id),
        'direccion': 'Carrer dels Esports, Barcelona, Spain',
        'latitud': 41.4010277,
        'longitud': 2.1119529999999713,
        'especialidad': Especialidad.objects.first() if Especialidad.objects.exists() else crear_especialidad(),
        'ultimo_curso_academico_superado': enums.CURSO_ACADEMICO[0][0],
        'descripcion': 'Lorem Ipsum Dolor Sit Amet',
        'busca_trabajo': True,
        'disponibilidad': enums.DISPONIBILIDAD[0][0],
        'nivel_de_privacidad': enums.NIVEL_DE_PRIVACIDAD[0][0]
    }
    est = Estudiante.objects.create(**datos)

    cts = ConocimientoTecnico.objects.all()[:5] if ConocimientoTecnico.objects.exists() else [crear_conocimiento()]
    for ct in cts:
        EstudianteTieneConocimientoTecnico.objects.create(estudiante=est, conocimiento=ct,
                                                          nivel=enums.NIVEL_DE_CONOCIMIENTO[0][0])

    ids = Idioma.objects.all()[:3] if Idioma.objects.exists() else [crear_idioma()]
    for i in ids:
        EstudianteHablaIdioma.objects.create(estudiante=est, idioma=i, nivel=enums.NIVEL_DE_CONOCIMIENTO[0][0])

    s = SectorDelMercado.objects.first() if SectorDelMercado.objects.exists() else crear_sector()
    EstudianteTieneExperienciaLaboral.objects.create(estudiante=est, sector=s, meses=3)

    return est

def crear_profesor(u):
    datos = {
        'usuario': u,
        'nombre': u.username,
        'departamento': Departamento.objects.first() if Departamento.objects.exists() else crear_departamento(),
        'url_upc': 'http://directori.upc.edu/directori/dadesPersona.jsp;jsessionid=B88FF6EEE9F066F2A826A87EA9FBF63E?id=100185{0}'.format(u.id%10)
    }
    prof = Profesor.objects.create(**datos)
    return prof

def crear_empresa(u, es_premium=False):
    datos = {
        'usuario': u,
        'nombre': u.username,
        'cif': str(u.id),
        'sector': SectorDelMercado.objects.first() if SectorDelMercado.objects.exists() else crear_sector(),
        'tamanyo': enums.TAMANYO_DE_EMPRESA[0][0],
        'direccion': 'Av Meridiana 234, Barcelona, Spain',
        'longitud': 41.4145023,
        'latitud': 2.1872143000000506,
        'descripcion': 'Lorem Ipsum Dolor Sit Amet',
        'esta_activa': True,
        'es_premium': es_premium
    }
    empr = Empresa.objects.create(**datos)
    return empr
