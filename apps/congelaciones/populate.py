from apps.congelaciones.models import Congelacion
from apps.ofertas.models import Oferta
from apps.usuarios.models import Perfil

for m in list(Oferta.objects.all())[-10:]:
    Congelacion.objects.create(modelo=m, motivo='Oferta erronea o fraudulenta')

m = Perfil.objects.all()[3]
Congelacion.objects.create(modelo=m, motivo='Perfil erroneo o fraudulenta')