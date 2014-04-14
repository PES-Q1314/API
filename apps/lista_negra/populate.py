from apps.lista_negra.models import ElementoDeLaListaNegra
from apps.usuarios.models import Empresa

# Las empresas son, de momento, los únicos modelos que pueden meterse en la lista negra. Una de ellas lo está
empresa = Empresa.objects.first()
ElementoDeLaListaNegra.objects.create(modelo=empresa,
                                      motivo='La descripción puede ser considerada como publicidad gratuita')