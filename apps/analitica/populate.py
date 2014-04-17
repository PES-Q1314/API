from apps.analitica.models import VisitaAOferta, VisitaAPerfil
from apps.ofertas.models import Oferta
from apps.usuarios.models import Perfil

ps = Perfil.objects.all()
os = Oferta.objects.all()

# Todos los perfiles visitan todas las ofertas
for p in ps:
    for o in os:
        VisitaAOferta.objects.create(perfil=p, oferta=o)

for p in ps:
    for p2 in ps:
        VisitaAPerfil.objects.create(perfil=p, perfil_visitado=p2)