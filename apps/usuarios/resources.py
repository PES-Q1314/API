# coding=utf-8
from apps.base.resources import ConocimientoTecnicoResource, SectorDelMercadoResource, IdiomaResource
from apps.congelaciones.resources import RecursoCongelable
from apps.denuncias.resources import RecursoDenunciable
from apps.lista_negra.resources import RecursoIncluibleEnLaListaNegra
from apps.usuarios.models import Estudiante, Profesor, Empresa, EstudianteTieneConocimientoTecnico, \
    EstudianteTieneExperienciaLaboral, EstudianteHablaIdioma
from core.action import action, response, ActionResourceMixin
from core.http import HttpOK
from core.resource import MetaGenerica
from tastypie import fields
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource


class EstudianteTieneConocimientoTecnicoResource(ModelResource):
    conocimiento = fields.ForeignKey(ConocimientoTecnicoResource, 'conocimiento', full=True)
    Meta = MetaGenerica(modelo=EstudianteTieneConocimientoTecnico)


class EstudianteTieneExperienciaLaboralResource(ModelResource):
    sector = fields.ForeignKey(SectorDelMercadoResource, 'sector', full=True)
    Meta = MetaGenerica(modelo=EstudianteTieneExperienciaLaboral)


class EstudianteHablaIdiomaResource(ModelResource):
    idioma = fields.ForeignKey(IdiomaResource, 'idioma', full=True)
    Meta = MetaGenerica(modelo=EstudianteHablaIdioma)


class EstudianteResource(RecursoDenunciable, RecursoCongelable, ModelResource):
    conocimientos_tecnicos = fields.ToManyField(EstudianteTieneConocimientoTecnicoResource,
                                                'conocimiento_tecnico_set', full=True)
    experiencia_laboral = fields.ToManyField(EstudianteTieneExperienciaLaboralResource,
                                             'experiencia_laboral_set', full=True)
    idiomas = fields.ToManyField(EstudianteHablaIdiomaResource, 'idioma_set', full=True)

    Meta = MetaGenerica(modelo=Estudiante)
    Meta.list_allowed_methods = ['get']
    Meta.detail_allowed_methods = ['get', 'patch']


class ProfesorResource(RecursoDenunciable, RecursoCongelable, ModelResource):
    Meta = MetaGenerica(modelo=Profesor)
    Meta.list_allowed_methods = ['get']
    Meta.detail_allowed_methods = ['get', 'patch']


class EmpresaResource(RecursoDenunciable, RecursoCongelable, RecursoIncluibleEnLaListaNegra, ActionResourceMixin,
                      ModelResource):
    Meta = MetaGenerica(modelo=Empresa)
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'put', 'patch', 'delete']

    @action(allowed=('post',), static=False)
    @response(HttpOK, "Pago correcto. Conversión a Premium realizada")
    def verificar_premium(self, request, clave_del_servicio_externo):
        # Nos conectamos al servicio premium y comprobamos que la clave_del_servicio_externo es correcta
        # De ser así, convertimos la empresa en Premium durante un año
        self._meta.object_class.objects.get(pk=request.api['pk']).convertir_en_premium()
        return self.create_response(request, {}, HttpOK)