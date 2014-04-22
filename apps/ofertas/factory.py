from datetime import date
from apps.base import enums
from apps.base.factory import crear_idioma, crear_conocimiento, crear_sector, crear_especialidad
from apps.base.models import ConocimientoTecnico, Idioma, SectorDelMercado, Especialidad
from apps.ofertas.models import OfertaDeEmpresa, RequisitoDeConocimientoTecnico, RequisitoDeIdioma, \
    RequisitoDeExperienciaLaboral, OfertaDeDepartamento, OfertaDeProyectoEmprendedor
from apps.usuarios.factory import crear_empresa, crear_profesor, crear_estudiante
from apps.usuarios.models import Empresa, Profesor, Estudiante

DATOS_OBLIGATORIOS_OFERTA = {
    'titulo': 'Oferta',
    'descripcion': 'Lorem Ipsum Dolor Sit Amet',
    'fecha_de_incorporacion': date.today(),
    'numero_de_puestos_vacantes': 4,
    'horario': enums.HORARIO_DE_TRABAJO[0][0],
    'tipo_de_jornada': enums.JORNADA_LABORAL[1][0],
    'ultimo_curso_academico_superado': enums.CURSO_ACADEMICO[0][0]
}


def crear_oferta_de_empresa(i=1):
    datos = {
        'titulo': 'Oferta de Empresa {0}'.format(i),
        'descripcion': 'Lorem Ipsum Dolor Sit Amet',
        'puesto': 'Community Manager',
        'meses_de_duracion': 4,
        'fecha_de_incorporacion': date.today(),
        'numero_de_puestos_vacantes': 4,
        'horario': enums.HORARIO_DE_TRABAJO[0][0],
        'tipo_de_jornada': enums.JORNADA_LABORAL[1][0],
        'ultimo_curso_academico_superado': enums.CURSO_ACADEMICO[0][0],
        'direccion': 'Avinguda Diagonal 34, Barcelona, Spain',
        'latitud': 41.4102793,
        'longitud': 2.2131842999999662,
        'usuario': Empresa.objects.first() if Empresa.objects.exists() else crear_empresa(),
        'hay_posibilidad_de_tfg': False,
        'salario_mensual': 600,
        'persona_de_contacto': 'Enric Margot',
        'email_de_contacto': 'enric.margot@gmail.com'
    }
    of = OfertaDeEmpresa.objects.create(**datos)

    cts = ConocimientoTecnico.objects.all()[:5] if ConocimientoTecnico.objects.exists() else [crear_conocimiento()]
    for ct in cts:
        RequisitoDeConocimientoTecnico.objects.create(oferta=of, conocimiento=ct,
                                                      nivel=enums.NIVEL_DE_CONOCIMIENTO[0][0])

    ids = Idioma.objects.all()[:3] if Idioma.objects.exists() else [crear_idioma()]
    for i in ids:
        RequisitoDeIdioma.objects.create(oferta=of, idioma=i, nivel=enums.NIVEL_DE_CONOCIMIENTO[0][0])

    s = SectorDelMercado.objects.first() if SectorDelMercado.objects.exists() else crear_sector()
    RequisitoDeExperienciaLaboral.objects.create(oferta=of, sector=s, meses=12)

    e = Especialidad.objects.first() if Especialidad.objects.exists() else crear_especialidad()
    of.especialidades.add(e)
    of.save()
    return of


def crear_oferta_de_departamento(i=1):
    datos = {
        'titulo': 'Oferta de Departamento {0}'.format(i),
        'descripcion': 'Lorem Ipsum Dolor Sit Amet',
        'puesto': 'Community Manager',
        'meses_de_duracion': 4,
        'fecha_de_incorporacion': date.today(),
        'numero_de_puestos_vacantes': 4,
        'horario': enums.HORARIO_DE_TRABAJO[0][0],
        'ultimo_curso_academico_superado': enums.CURSO_ACADEMICO[0][0],
        'direccion': 'Avinguda Diagonal 34, Barcelona, Spain',
        'latitud': 41.4102793,
        'longitud': 2.2131842999999662,
        'usuario': Profesor.objects.first() if Profesor.objects.exists() else crear_profesor()
    }
    of = OfertaDeDepartamento.objects.create(**datos)

    cts = ConocimientoTecnico.objects.all()[:5] if ConocimientoTecnico.objects.exists() else [crear_conocimiento()]
    for ct in cts:
        RequisitoDeConocimientoTecnico.objects.create(oferta=of, conocimiento=ct,
                                                      nivel=enums.NIVEL_DE_CONOCIMIENTO[0][0])

    e = Especialidad.objects.first() if Especialidad.objects.exists() else crear_especialidad()
    of.especialidades.add(e)
    of.save()
    return of


def crear_oferta_de_proyecto_emprendedor(i=1):
    datos = {
        'titulo': 'Oferta de Proyecto Emprendedor {0}'.format(i),
        'descripcion': 'Lorem Ipsum Dolor Sit Amet',
        'puesto': 'Community Manager',
        'meses_de_duracion': 4,
        'fecha_de_incorporacion': date.today(),
        'numero_de_puestos_vacantes': 4,
        'horario': enums.HORARIO_DE_TRABAJO[0][0],
        'direccion': 'Avinguda Diagonal 34, Barcelona, Spain',
        'latitud': 41.4102793,
        'longitud': 2.2131842999999662,
        'usuario': Estudiante.objects.first() if Estudiante.objects.exists() else crear_estudiante()
    }
    of = OfertaDeProyectoEmprendedor.objects.create(**datos)
    e = Especialidad.objects.first() if Especialidad.objects.exists() else crear_especialidad()
    of.especialidades.add(e)
    of.save()
    return of