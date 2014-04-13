from datetime import date
from apps.base import enums
from apps.base.models import Especialidad, ConocimientoTecnico, Idioma, SectorDelMercado, Departamento
from apps.cuentas.models import SystemUser
from apps.usuarios.models import Estudiante, EstudianteTieneConocimientoTecnico, EstudianteHablaIdioma, \
    EstudianteTieneExperienciaLaboral, Profesor, Empresa

# Obtenemos todos los usuarios y los agrupamos de 3 en 3 (para tener tres de cada tipo de perfiles, y el resto administradores)
usuarios = SystemUser.objects.all()
chunks = lambda l, n: [l[x: x + n] for x in xrange(0, len(l), n)]
grupo = chunks(usuarios, 3)

# CREAMOS ESTUDIANTES
for u in grupo[0]:
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
        'especialidad': Especialidad.objects.first(),
        'ultimo_curso_academico_superado': enums.CURSO_ACADEMICO[0][0],
        'descripcion': 'Lorem Ipsum Dolor Sit Amet',
        'busca_trabajo': True,
        'disponibilidad': enums.DISPONIBILIDAD[0][0],
        'nivel_de_privacidad': enums.NIVEL_DE_PRIVACIDAD
    }
    est = Estudiante.objects.create(**datos)

    for ct in ConocimientoTecnico.objects.all()[:5]:
        EstudianteTieneConocimientoTecnico.objects.create(estudiante=est, conocimiento=ct,
                                                          nivel=enums.NIVEL_DE_CONOCIMIENTO[0][0])

    for i in Idioma.objects.all()[:3]:
        EstudianteHablaIdioma.objects.create(estudiante=est, idioma=i, nivel=enums.NIVEL_DE_CONOCIMIENTO[0][0])

    s = SectorDelMercado.objects.first()
    EstudianteTieneExperienciaLaboral.objects.create(estudiante=est, sector=s, meses=3)

# CREAMOS PROFESORES
for u in grupo[1]:
    datos = {
        'usuario': u,
        'nombre': u.username,
        'departamento': Departamento.objects.first(),
        'url_upc': 'http://directori.upc.edu/directori/dadesPersona.jsp;jsessionid=B88FF6EEE9F066F2A826A87EA9FBF63E?id=100185{0}'.format(u.id%10)
    }
    prof = Profesor.objects.create(**datos)


# CREAMOS EMPRESAS
for u in grupo[2]:
    datos = {
        'usuario': u,
        'nombre': u.username,
        'cif': str(u.id),
        'sector': SectorDelMercado.objects.first(),
        'tamanyo': enums.TAMANYO_DE_EMPRESA[0][0],
        'direccion': 'Av Meridiana 234, Barcelona, Spain',
        'longitud': 41.4145023,
        'latitud': 2.1872143000000506,
        'descripcion': 'Lorem Ipsum Dolor Sit Amet',
        'esta_activa': True
    }
    empr = Empresa.objects.create(**datos)
