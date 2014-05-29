from apps.cuentas.models import SystemUser


def crear_usuario(nombre, i):
    u = '{0}{1}'.format(nombre, i)
    e = '{0}@upc.edu'.format(u)
    SystemUser.objects.create_user(username=u, email=e, password='1234')

for tipo in ['estudiante', 'profesor', 'empresa', 'admin']:
    for i in range(3):
        crear_usuario(tipo, i+1)
