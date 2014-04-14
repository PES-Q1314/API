from datetime import date
from apps.base import enums
from apps.base.models import ConocimientoTecnico, Idioma, SectorDelMercado, Especialidad
from apps.ofertas.models import Oferta, RequisitoDeConocimientoTecnico, RequisitoDeIdioma, RequisitoDeExperienciaLaboral, \
    OfertaDeEmpresa, OfertaDeDepartamento, OfertaDeProyectoEmprendedor
from apps.usuarios.models import Empresa, Profesor, Estudiante

# CREAMOS OFERTAS DE EMPRESA
for i in range(50):
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
        'autor': Empresa.objects.first(),
        'hay_posibilidad_de_tfg': False,
        'salario_mensual': 600,
        'persona_de_contacto': 'Enric Margot',
        'email_de_contacto': 'enric.margot@gmail.com'
    }
    of = OfertaDeEmpresa.objects.create(**datos)

    for ct in ConocimientoTecnico.objects.all()[1:5]:
        RequisitoDeConocimientoTecnico.objects.create(oferta=of, conocimiento=ct,
                                                          nivel=enums.NIVEL_DE_CONOCIMIENTO[0][0])

    for i in Idioma.objects.all()[1:4]:
        RequisitoDeIdioma.objects.create(oferta=of, idioma=i, nivel=enums.NIVEL_DE_CONOCIMIENTO[0][0])

    s = SectorDelMercado.objects.first()
    RequisitoDeExperienciaLaboral.objects.create(oferta=of, sector=s, meses=12)

    of.especialidades.add(Especialidad.objects.first())
    of.save()


# CREAMOS OFERTAS DE DEPARTAMENTO
for i in range(50):
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
        'autor': Profesor.objects.first()
    }
    of = OfertaDeDepartamento.objects.create(**datos)

    for ct in ConocimientoTecnico.objects.all()[1:5]:
        RequisitoDeConocimientoTecnico.objects.create(oferta=of, conocimiento=ct,
                                                          nivel=enums.NIVEL_DE_CONOCIMIENTO[0][0])

    of.especialidades.add(Especialidad.objects.first())
    of.save()


# CREAMOS OFERTAS DE PROYECTOS EMPRENDEDORES
for i in range(50):
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
        'autor': Estudiante.objects.first()
    }
    of = OfertaDeProyectoEmprendedor.objects.create(**datos)
    of.especialidades.add(Especialidad.objects.first())
    of.save()
