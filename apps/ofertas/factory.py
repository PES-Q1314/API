import datetime
import random
from apps.base import enums
from apps.base.factory import crear_conocimiento, crear_especialidad, crear_idioma, crear_sector
from apps.base.models import ConocimientoTecnico, Idioma, SectorDelMercado, Especialidad
from apps.ofertas.models import OfertaDeEmpresa, RequisitoDeConocimientoTecnico, RequisitoDeIdioma, \
    RequisitoDeExperienciaLaboral, OfertaDeDepartamento, OfertaDeProyectoEmprendedor
from apps.usuarios.models import Empresa, Profesor, Estudiante


PUESTOS = ['Community Manager', 'Analista de sistemas', 'Arquitecto', 'Administrador de Bases de Datos', 'Diseñador gráfico', 'Ingeniero químico', 'Ingeniero mecánico', 'Ingeniero bioquímico', 'Desarrollador', 'Programador', 'Project manager', 'Experto en Marketing']
DIRECCIONES = ['C/ Esports 1', 'Avg Diagonal 213', 'Av Meridiana 187', 'Plç Espanya 3', 'C/ Mallorca 43',
               'C/ Balmes 3', 'Passeig de Gracia, 34']
DESCRIPCIONES = [
    'El perfil corresponde al puesto de {0} para desempeñar distintas tareas dentro de nuestro proyecto. Trabajamos en un mercado en plena expansión, en un entorno de trabajo joven y dinámico donde podrán participar en innovadores proyectos que permitirán completar su formación y potenciar sus capacidades.',
    'Buscamos varias personas con el perfil de {0}. El proyecto principal que ha generado esa necesidad es una empresa internacional con presencia fuerte en el mercado nacional. El idioma del proyecto será el castellano.',
    'Buscamos una persona dinámica, con espíritu emprendedor e iniciativa, alta capacidad de trabajo, clara orientación hacia el cliente y con un importante nivel de ambición profesional (altas posibilidades de crecer profesionalmente conjuntamente con el proyecto empresarial).',
    'Nuestro principal activo consiste en contar con un equipo humano de alto nivel técnico y plenamente motivado, con un equipo directivo con amplia experiencia en el sector, siendo por lo tanto los principales compromisos, la calidad, la innovación, y el desarrollo de nuestros profesionales.'
]
CONTACTOS = ['Enric Margot', 'Paola Vivian', 'Ernest Martinez', 'Mollie Lago', 'Robert Stevenson', 'Chen Li']

CONOCIMIENTOS = list(ConocimientoTecnico.objects.all()) if ConocimientoTecnico.objects.exists() else [crear_conocimiento()]
SECTORES = list(SectorDelMercado.objects.all()) if SectorDelMercado.objects.exists() else [crear_sector()]
IDIOMAS = list(Idioma.objects.all()) if Idioma.objects.exists() else [crear_idioma()]
ESPECIALIDADES = list(Especialidad.objects.all()) if Especialidad.objects.exists() else [crear_especialidad()]



def datos_generales_oferta():
    p = random.choice(PUESTOS)
    return {
        'titulo': p,
        'descripcion': random.choice(DESCRIPCIONES).format(p),
        'puesto': p,
        'meses_de_duracion': random.randint(1, 12),
        'fecha_de_incorporacion': datetime.date.today() + datetime.timedelta(weeks=random.randint(1, 52)),
        'numero_de_puestos_vacantes': random.randint(1, 6),
        'horario': random.choice(enums.HORARIO_DE_TRABAJO)[0],
        'tipo_de_jornada': random.choice(enums.JORNADA_LABORAL)[0],
        'tipo_de_contrato': random.choice(enums.TIPO_DE_CONTRATO)[0],
        'ultimo_curso_academico_superado': random.choice(enums.CURSO_ACADEMICO)[0],
        'direccion': random.choice(DIRECCIONES),
        'latitud': 41.4102793,
        'longitud': 2.2131842999999662,
    }


def incluir_extras(of):
    for i in range(5):
        RequisitoDeConocimientoTecnico.objects.get_or_create(oferta=of, conocimiento=random.choice(CONOCIMIENTOS),
                                                             nivel=random.choice(enums.NIVEL_DE_CONOCIMIENTO)[0])
        RequisitoDeIdioma.objects.get_or_create(oferta=of, idioma=random.choice(IDIOMAS),
                                                             nivel=random.choice(enums.NIVEL_DE_CONOCIMIENTO)[0])
        RequisitoDeExperienciaLaboral.objects.get_or_create(oferta=of, sector=random.choice(SECTORES),
                                                             meses=random.randint(1, 12))
        of.especialidades.add(random.choice(ESPECIALIDADES))

    for b in of.beneficios_laborales.__dict__:
        b = random.choice([True, False, False])

    of.save()



DATOS_OBLIGATORIOS_OFERTA = datos_generales_oferta()


def crear_oferta_de_empresa(u=random.choice(list(Empresa.objects.all())), extras=True):
    datos = datos_generales_oferta()
    c = random.choice(CONTACTOS)
    datos.update({
        'usuario': u,
        'hay_posibilidad_de_tfg': random.choice([True, False]),
        'salario_mensual': random.randint(400, 1400),
        'persona_de_contacto': c,
        'email_de_contacto': '{0}.{1}@gmail.com'.format(c.split()[0][0].lower(), c.split()[1].lower()) # 'Enric Margot' to 'e.margot@gmail.com'
    })
    of = OfertaDeEmpresa.objects.create(**datos)
    if extras:
        incluir_extras(of)
    return of


def crear_oferta_de_departamento(u=random.choice(list(Profesor.objects.all())), extras=True):
    datos = datos_generales_oferta()
    datos.update({'usuario': u})
    of = OfertaDeDepartamento.objects.create(**datos)
    if extras:
        incluir_extras(of)
    return of


def crear_oferta_de_proyecto_emprendedor(u=random.choice(list(Estudiante.objects.all())), extras=True):
    datos = datos_generales_oferta()
    datos.update({'usuario': u})
    of = OfertaDeProyectoEmprendedor.objects.create(**datos)
    if extras:
        incluir_extras(of)
    return of