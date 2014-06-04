from apps.ofertas.factory import crear_oferta_de_empresa, crear_oferta_de_departamento, \
    crear_oferta_de_proyecto_emprendedor

# CREAMOS TODOS LOS TIPOS DE OFERTA
for i in range(15):
    crear_oferta_de_empresa()
    crear_oferta_de_departamento()
    crear_oferta_de_proyecto_emprendedor()
