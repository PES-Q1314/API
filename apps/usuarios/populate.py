from apps.cuentas.models import SystemUser
from apps.usuarios.factory import crear_estudiante, crear_profesor, crear_empresa

# Obtenemos todos los usuarios y los agrupamos de 3 en 3 (para tener tres de cada tipo de perfiles, y el resto administradores)
usuarios = SystemUser.objects.all()
chunks = lambda l, n: [l[x: x + n] for x in range(0, len(l), n)]
grupo = chunks(usuarios, 3)

# CREAMOS ESTUDIANTES
for u in grupo[0]:
    crear_estudiante(u)


# CREAMOS PROFESORES
for u in grupo[1]:
    crear_profesor(u)


# CREAMOS EMPRESAS
for u in grupo[2]:
    crear_empresa(u)
