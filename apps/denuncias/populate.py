from apps.denuncias.models import Denuncia
from apps.ofertas.models import Oferta
from apps.usuarios.models import Estudiante


# Escogemos estudiantes que denuncian ofertas
estudiantes = list(Estudiante.objects.all())
ofertas = list(Oferta.objects.all())

for i, est in enumerate(estudiantes):
    for j in range(3):
        Denuncia.objects.create(denunciante=est, modelo=ofertas[(i*7+j) % len(ofertas)])