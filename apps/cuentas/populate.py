from apps.cuentas.models import SystemUser

for i in range(12):
    u = 'usuario{0}'.format(i)
    e = '{0}@upc.edu'.format(u)
    SystemUser.objects.create_user(username=u, email=e, password='1234')