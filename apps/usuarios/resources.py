# coding=utf-8
from apps.base.resources import ConocimientoTecnicoResource, SectorDelMercadoResource, IdiomaResource
from apps.congelaciones.resources import RecursoCongelable
from apps.denuncias.resources import RecursoDenunciable
from apps.lista_negra.resources import RecursoIncluibleEnLaListaNegra
from apps.usuarios.authorizations import OpenProfileAuth, ClosedProfileAuth, EstudiantePlusAuth
from apps.usuarios.models import Estudiante, Profesor, Empresa, EstudianteTieneConocimientoTecnico, \
    EstudianteTieneExperienciaLaboral, EstudianteHablaIdioma, Perfil
from core.accion import action, response, ActionResourceMixin
from core.autorizacion import es_admin
from core.http import HttpOK
from core.recurso import MetaGenerica
from tastypie import fields
from tastypie.exceptions import Unauthorized, ImmediateHttpResponse
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource



class EstudianteResource(RecursoDenunciable, RecursoCongelable, ModelResource):
    conocimientos_tecnicos = fields.ToManyField('apps.usuarios.resources.EstudianteTieneConocimientoTecnicoResource',
                                                'conocimiento_tecnico_set', full=True, null=True)
    experiencia_laboral = fields.ToManyField('apps.usuarios.resources.EstudianteTieneExperienciaLaboralResource',
                                             'experiencia_laboral_set', full=True, null=True)
    idiomas = fields.ToManyField('apps.usuarios.resources.EstudianteHablaIdiomaResource', 'idioma_set', full=True, null=True)

    Meta = MetaGenerica(modelo=Estudiante)
    Meta.authorization = ClosedProfileAuth()


class ProfesorResource(RecursoDenunciable, RecursoCongelable, ModelResource):
    Meta = MetaGenerica(modelo=Profesor)
    Meta.authorization = ClosedProfileAuth()


class EmpresaResource(RecursoDenunciable, RecursoCongelable, RecursoIncluibleEnLaListaNegra, ActionResourceMixin,
                      ModelResource):
    Meta = MetaGenerica(modelo=Empresa)
    Meta.authorization = OpenProfileAuth()

    # Asociamos la creación de un perfil al usuario que hace la request
    def obj_create(self, bundle, **kwargs):
        return super().obj_create(bundle, usuario=bundle.request.user)

    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Pago correcto. Conversión a Premium realizada")
    @response(HttpUnauthorized, "No está autorizado para realizar modificaciones sobre este elemento")
    def verificar_premium(self, request, clave_del_servicio_externo):
        empresa = self._meta.object_class.objects.get(pk=request.api['pk'])
        if empresa.usuario != request.user:
            raise ImmediateHttpResponse(HttpUnauthorized())

        # Nos conectamos al servicio premium y comprobamos que la clave_del_servicio_externo es correcta
        # De ser así, convertimos la empresa en Premium durante un año
        empresa.convertir_en_premium()
        return self.create_response(request, {}, HttpOK)

    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Empresa aceptada")
    @response(HttpUnauthorized, "No está autorizado para realizar esta acción")
    def aceptar(self, request):
        if not es_admin(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())

        self._meta.object_class.objects.get(pk=request.api['pk']).aceptar()
        return self.create_response(request, {}, HttpOK)

    @action(allowed=('post',), static=False, login_required=True)
    @response(HttpOK, "Empresa rechazada y eliminada")
    @response(HttpUnauthorized, "No está autorizado para realizar esta acción")
    def rechazar(self, request):
        if not es_admin(request.user):
            raise ImmediateHttpResponse(HttpUnauthorized())

        self._meta.object_class.objects.get(pk=request.api['pk']).rechazar()
        return self.create_response(request, {}, HttpOK)




##################
# RELACIONES M2M #
##################

class EstudiantePlusMixin(ModelResource):
    # Asociamos la creación de una relación al perfil del estudiante que hace la request
    def obj_create(self, bundle, **kwargs):
        p = Perfil.objects.get_subclass(usuario=bundle.request.user)
        if isinstance(p, Estudiante):
            return super().obj_create(bundle, estudiante=p)
        else:
            raise ImmediateHttpResponse(HttpUnauthorized())

class EstudianteTieneConocimientoTecnicoResource(EstudiantePlusMixin, ModelResource):
    conocimiento = fields.ForeignKey(ConocimientoTecnicoResource, 'conocimiento', full=True)
    Meta = MetaGenerica(modelo=EstudianteTieneConocimientoTecnico)
    Meta.authorization = EstudiantePlusAuth()


class EstudianteTieneExperienciaLaboralResource(EstudiantePlusMixin, ModelResource):
    sector = fields.ForeignKey(SectorDelMercadoResource, 'sector', full=True)
    Meta = MetaGenerica(modelo=EstudianteTieneExperienciaLaboral)
    Meta.authorization = EstudiantePlusAuth()


class EstudianteHablaIdiomaResource(EstudiantePlusMixin, ModelResource):
    idioma = fields.ForeignKey(IdiomaResource, 'idioma', full=True)
    Meta = MetaGenerica(modelo=EstudianteHablaIdioma)
    Meta.authorization = EstudiantePlusAuth()
