from datetime import date
import random
from apps.base import enums
from apps.base.factory import crear_especialidad, crear_departamento, crear_sector, crear_conocimiento, crear_idioma
from apps.base.models import Especialidad, ConocimientoTecnico, Idioma, SectorDelMercado, Departamento
from apps.usuarios.models import Estudiante, EstudianteTieneConocimientoTecnico, EstudianteHablaIdioma, \
    EstudianteTieneExperienciaLaboral, Profesor, Empresa, Administrador

RANDSEED = 1234  # Use 'static' seed to generate always the same profiles.
random.seed(RANDSEED)  # Use None to produce different profiles every time.

NOMBRES = ['Maria', 'Anna', 'Xavi', 'Roberto', 'Marc', 'Eduard', 'Hector', 'Francesc', 'Laura']
APELLIDOS = ['Matas', 'Llorca', 'Borges', 'Capdevila', 'Fernandez', 'Martinez', 'Garcia', 'Jimenez']
EMPRESAS = [' IPS', 'BASA', 'AGBAR', 'Vanadys Solutions', 'Digital Response', 'SIVICOM SYSTEMS']
DIRECCIONES = ['C/ Esports 1', 'Avg Diagonal 213', 'Av Meridiana 187', 'Plç Espanya 3', 'C/ Mallorca 43',
               'C/ Balmes 3', 'Passeig de Gracia, 34']
DESCR_ESTUDIANTES = [
    'Soy un estudiante de tercero de Ingeniería Informática, con amplios conocimientos en el mundo web, deseando de aprender y adquirir experiencia laboral en una empresa con proyectos interesantes',
    'Antiguo alumno de la facultad de arquitectura de la UPC, interesado en proyectos de urbanismo y diseño de estructuras orientadas al ciudadano',
    'Estudio ingeniería industrial, segundo año. Soy una apasionada de la ingeniería mecánica, y me gustaría encontrar un trabajo que me permitiera adquirir más experiencia y aplicar mis conocimientos en ese campo',
    'I\m from Israel. I\'m currently studying a master in Marketing and Communication, and specialize in gathering people from different backgrounds and consituting teams to create a techlology start-up'
]
DESCR_EMPRESAS = [
    'Som una empresa informàtica i tecnològica formada al 1986, líder al seu sector d\'activitat. Comptem amb una base molt sòlida de productes, clients i serveis que ens permeten innovar i potenciar el nostre creixement i activitat tecnològica. ',
    'Líder global en consultoría tecnológica e innovación, con una red internacional de 21.000 profesionales en todo el mundo, selecciona INGENIEROS /AS DE SOFTWARE con experiencia en MICROSOFT .NET en Girona y Barcelona para el desarrollo de proyectos en nuestros clientes de multiples sectores, media, farma, etc. ',
    'Som una spin-off de la UPC amb un producte de monitoratge de tràfic IP que estem ja comercialitzant (avui per avui, el nostre client més gran és la xarxa acadèmica espanyola, RedIRIS). Oferim el nostre producte tant com a "appliance" tradicional per a grans empreses, com en modalitat "software as a service" per a clients amb xarxes més reduïdes. ',
    'C de auditoría de sistemas y procesos, cuyo objetivo es utilizar herramientas de data mining y metodología de auditoría para optimizar los procesos de negocio de nuestros clientes. Trabajamos en todo tipo de sectores, destacando el sector bancario y sector industrial (fabricación y distribución), en el ámbito catalán. Nuestros perfiles son de analistas de datos, si bien buscamos un perfil programador que además de realizar las tareas propias de analista de datos y procesos, tenga capacidad para la implementación de aplicaciones relacionadas con nuestro negocio.',
    'Engeneering company specialized on developing new product for a wide range of sectors. The company is part of the group Ficosa (www.ficosa.com ).'
]

CONOCIMIENTOS = list(ConocimientoTecnico.objects.all()) if ConocimientoTecnico.objects.exists() else [crear_conocimiento()]
SECTORES = list(SectorDelMercado.objects.all()) if SectorDelMercado.objects.exists() else [crear_sector()]
IDIOMAS = list(Idioma.objects.all()) if Idioma.objects.exists() else [crear_idioma()]
ESPECIALIDADES = list(Especialidad.objects.all()) if Especialidad.objects.exists() else [crear_especialidad()]
DEPARTAMENTOS = list(Departamento.objects.all()) if Departamento.objects.exists() else [crear_departamento()]

ULTIMA_EMPRESA_UTILIZADA = [-1]
NOMBRES_UTILIZADOS = []

def incluir_extras(est):
    for i in range(5):
        EstudianteTieneConocimientoTecnico.objects.get_or_create(estudiante=est, conocimiento=random.choice(CONOCIMIENTOS),
                                                             nivel=random.choice(enums.NIVEL_DE_CONOCIMIENTO)[0])
        EstudianteHablaIdioma.objects.get_or_create(estudiante=est, idioma=random.choice(IDIOMAS),
                                                             nivel=random.choice(enums.NIVEL_DE_CONOCIMIENTO)[0])
        EstudianteTieneExperienciaLaboral.objects.get_or_create(estudiante=est, sector=random.choice(SECTORES),
                                                             meses=random.randint(1, 12))
    est.save()

def obtener_empresa():
    ULTIMA_EMPRESA_UTILIZADA[0] += 1
    ult = ULTIMA_EMPRESA_UTILIZADA[0]
    if ult >= len(EMPRESAS):
        n = '{0}{1}'.format(random.choice(EMPRESAS), ult)
    else:
        n = EMPRESAS[ult]
    return n

def obtener_nombre():
    n = '{0} {1}'.format(random.choice(NOMBRES), random.choice(APELLIDOS))
    while n in NOMBRES_UTILIZADOS:
        n = '{0} {1}'.format(random.choice(NOMBRES), random.choice(APELLIDOS))
    NOMBRES_UTILIZADOS.append(n)
    return n


def crear_estudiante(u):
    datos = {
        'usuario': u,
        'nombre': obtener_nombre(),
        'dni': str(u.id),
        'fecha_de_nacimiento': date(day=random.randint(1, 30), month=random.randint(1, 12), year=random.randint(1985, 1996)),
        'sexo': random.choice(enums.SEXO)[0],
        'telefono': str(600123456 + u.id),
        'direccion': random.choice(DIRECCIONES),
        'latitud': 41.4010277,
        'longitud': 2.1119529999999713,
        'especialidad': random.choice(ESPECIALIDADES),
        'ultimo_curso_academico_superado': random.choice(enums.CURSO_ACADEMICO)[0],
        'descripcion': random.choice(DESCR_ESTUDIANTES),
        'busca_trabajo': True,
        'disponibilidad': random.choice(enums.DISPONIBILIDAD)[0],
        'nivel_de_privacidad': random.choice(enums.NIVEL_DE_PRIVACIDAD)[0]
    }
    est = Estudiante.objects.create(**datos)
    incluir_extras(est)
    return est

def crear_profesor(u):
    datos = {
        'usuario': u,
        'nombre': obtener_nombre(),
        'departamento': random.choice(DEPARTAMENTOS),
        'url_upc': 'http://directori.upc.edu/directori/dadesPersona.jsp;jsessionid=B88FF6EEE9F066F2A826A87EA9FBF63E?id=100185{0}'.format(u.id%10)
    }
    prof = Profesor.objects.create(**datos)
    return prof

def crear_empresa(u, es_premium=False):
    datos = {
        'usuario': u,
        'nombre': obtener_empresa(),
        'cif': str(u.id),
        'sector': random.choice(SECTORES),
        'tamanyo': random.choice(enums.TAMANYO_DE_EMPRESA)[0],
        'direccion': random.choice(DIRECCIONES),
        'longitud': 41.4145023,
        'latitud': 2.1872143000000506,
        'descripcion': random.choice(DESCR_EMPRESAS),
        'esta_activa': True,
        'es_premium': es_premium
    }
    empr = Empresa.objects.create(**datos)
    return empr


def crear_administrador(u):
    datos = {
        'usuario': u,
        'nombre': obtener_nombre(),
    }
    admin = Administrador.objects.create(**datos)
    return admin
