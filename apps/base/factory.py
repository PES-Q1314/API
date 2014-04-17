from apps.base.models import Idioma, ConocimientoTecnico, SectorDelMercado, Departamento, Especialidad


def crear_idioma():
    return Idioma.objects.create(codigo='zz', idioma='Zazimbauense')

def crear_conocimiento():
    return ConocimientoTecnico.objects.create(conocimiento='zz')

def crear_sector():
    return SectorDelMercado.objects.create(sector='zz')

def crear_departamento():
    return Departamento.objects.create(siglas='zz', nombre='zzz', url_upc='http://www.zz.com')

def crear_especialidad():
    return Especialidad.objects.create(nombre='zz', facultad='zzz', url_upc='http://www.zz.com')