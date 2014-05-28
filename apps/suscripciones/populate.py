from apps.ofertas.models import Oferta
from apps.suscripciones.models import Suscripcion
from apps.usuarios.models import Estudiante

# Escogemos estudiantes y ofertas, que son dos de los modelos que pueden ejercer esta funcionalidad
estudiantes = list(Estudiante.objects.all())
ofertas = list(Oferta.objects.all().select_subclasses())


for i, est in enumerate(estudiantes):
    for j in range(10):
        of = ofertas[(i+j*23) % len(ofertas)]
        if of.usuario != est:
            Suscripcion.objects.create(suscriptor=est, modelo=of)