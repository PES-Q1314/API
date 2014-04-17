from datetime import date
from apps.base import enums
from apps.base.models import ConocimientoTecnico, Idioma, SectorDelMercado, Especialidad
from apps.ofertas.factory import crear_oferta_de_empresa, crear_oferta_de_departamento, \
    crear_oferta_de_proyecto_emprendedor
from apps.ofertas.models import Oferta, RequisitoDeConocimientoTecnico, RequisitoDeIdioma, RequisitoDeExperienciaLaboral, \
    OfertaDeEmpresa, OfertaDeDepartamento, OfertaDeProyectoEmprendedor
from apps.usuarios.models import Empresa, Profesor, Estudiante

# CREAMOS OFERTAS DE EMPRESA
for i in range(50):
    crear_oferta_de_empresa(i)


# CREAMOS OFERTAS DE DEPARTAMENTO
for i in range(50):
    crear_oferta_de_departamento(i)


# CREAMOS OFERTAS DE PROYECTOS EMPRENDEDORES
for i in range(50):
    crear_oferta_de_proyecto_emprendedor(i)
