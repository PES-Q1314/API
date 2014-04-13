from apps.ofertas.models import Oferta
from apps.suscripciones.models import Suscripcion
from apps.usuarios.models import Estudiante

# Escogemos estudiantes y ofertas, que son dos de los modelos que pueden ejercer esta funcionalidad
estudiantes = list(Estudiante.objects.all())
ofertas = list(Oferta.objects.all())


for i, est in enumerate(estudiantes):
    for j in range(10):
        Suscripcion.objects.create(autor=est, modelo=ofertas[(i*5+j) % len(ofertas)])