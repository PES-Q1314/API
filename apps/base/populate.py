# coding=utf-8
from apps.base.datos import departamentos, estudios, idiomas
from apps.base.models import Idioma, ConocimientoTecnico, Departamento, Especialidad, SectorDelMercado

# Introducimos todos los idiomas
for idioma in idiomas.ISO_639_1:
    print('a')
    Idioma.objects.create(codigo=idioma[0], idioma=idioma[1])


# Introducimos todos los departamentos
for dpt in departamentos.NOMBRES:
    Departamento.objects.create(siglas=dpt[0], nombre=dpt[1], url_upc=departamentos.URL_UPC.format(dpt[2]))

# Introducimos todos los estudios
for estudio in estudios.ESTUDIOS:
    Especialidad.objects.create(nombre=estudio[0], facultad=estudio[-2], url_upc=estudios.URL_UPC.format(estudio[-1]))


conocimientos_tecnicos = ['c', 'c++', 'MongoDB', 'Python', 'Ruby', '.NET', 'Oracle', 'R', 'MySQL', 'JavaScript', 'Java',
                          'Mecánica', 'Gestión de Proyectos', 'Impresión 3D', 'Maple', 'Cálculo de estructuras']
for ct in conocimientos_tecnicos:
    ConocimientoTecnico.objects.create(conocimiento=ct)


sectores = ['Consultoría', 'Urbanismo', "Auditoría", 'Agricultura', 'Industria', 'Diseño gráfico']
for s in sectores:
    SectorDelMercado.objects.create(sector=s)


