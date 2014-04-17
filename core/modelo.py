
def resolver_usuario(obj):
    u = obj
    while hasattr(u, 'usuario'):
        u = u.usuario
    return u
