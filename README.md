# API Bolsa de empleo universitaria
API REST implementada usando Python, Django y Tastypie, para dar soporte a la aplicación web de la nueva bolsa universitaria de la UPC

## Cómo utilizar la API

La API sigue las convenciones típicas de una API REST, pero al estar diseñada con Django + Tastypie hay algunos detalles para los cuales convendría mirarse la documentación específica de estos.

La interacción con la API sigue el siguiente patrón:
* `GET /api` Lista de todos los recursos de la API y su dirección (dónde se consultan o modifican)
* `GET /api/<recurso>` Devuelve una lista de las instancias de <recurso>
* `POST /api/<recurso>` Con los datos correctos, crea un <recurso> nuevo
* `GET /api/<recurso>/<id>/` Devuelve la información de un <recurso> concreto, dado su <id>
* `PATCH /api/<recurso>/<id>/` Actualiza uno o varios campos del <recurso> concreto identificado por <id>
* `DELETE /api/<recurso>/<id>/` Elimina el <recurso> concreto identificado por <id>
* `GET /api/<recurso>/schema` Provee meta-información sobre el recurso (qué se puede hacer con él y cómo). Es un poco críptico pero es la manera que tiene la API de auto-documentarse a sí misma, y es muy útil.

## Casos de uso implementados

1. __Autenticarse__. Un usuario, administrador, o miembro del equipo rectoral se autentica en el sistema, para tener acceso a él.
2. __Registrarse como empresa__. Una empresa se registra en el sistema.
3. __Validar nueva empresa__. Un administrador verifica los datos de una empresa y confirma o descarta su registro en el sistema.
4. __Gestionar perfil de usuario__. Un usuario modifica o elimina su perfil.
5. __Configurar opciones de privacidad__. Un estudiante decide qué opciones de privacidad quiere aplicar a su perfil.
6. __Configurar opciones de notificaciones__. Un estudiante decide qué notificaciones recibirá por correo electrónico.
7. __Enviar boletín informativo__. El sistema envía el boletín semanal de ofertas a los estudiantes que estén suscritos a él.
8. __Contratar servicio Premium__. Una empresa contrata el servicio Premium de la bolsa de empleo.
9. __Gestionar oferta__. Un usuario crea, modifica o elimina una de sus ofertas.
10. __Buscar usuario__. Un estudiante, profesor o empresa premium busca usuarios, en función de los filtros disponibles.
11. __Buscar oferta__. Un usuario busca ofertas, en función de los filtros disponibles.
12. __Suscribirse a oferta__. Un estudiante se suscribe a una oferta.
13. __Gestionar suscripciones emitidas__. Un estudiante consulta o cancela las suscripciones emitidas por él.
14. __Gestionar suscripciones recibidas__. Un usuario consulta, acepta o descarta las suscripciones recibidas por una de sus ofertas.
15. __Denunciar elemento__. Un estudiante denuncia cierto contenido de la página que considera inapropiado, y expresa el motivo.
16. __Administrar denuncia__. Un administrador consulta una denuncia sobre un elemento, y decide si la descarta o toma medidas acordes a ella (congelar o eliminar el contenido denunciado).
17. __Administrar modificaciones__. Un administrador consulta los contenidos modificados a raíz de una congelación y decide si estos ya cumplen con los requisitos de la página, siguen congelados, o deben eliminarse definitivamente.
18. __Administrar lista negra__. Un administrador añade o elimina una empresa de la lista negra.
19. __Solicitar ayuda__. Un usuario se dirige a la sección de ayuda y soporte para resolver sus dudas, contactar personalmente con un administrador, o concertar una cita presencial.



## Cómo modificar la API

### Pre-requisitos (todo lo que necesitas saber de…)

* [Django](https://www.djangoproject.com). La página tiene una guía de instalación y un tutorial geniales.
* [TastyPie](http://django-tastypie.readthedocs.org/en/latest/index.html). Un framework que facilita el trabajo con APIs REST encima de Django.


### ¿Qué hago si quiero modificar algo?

Para modificar algo de la API hay que seguir, a grandes rasgos, los siguientes pasos (en una terminal Unix):

1. Clonar el repositorio en una carpeta de elección
2. Instalar localmente un entorno virtualenv (idealmente llamado venv) y ejecutarlo
	1. cd `path_to_project` (misma carpeta que manage.py)
	2. `virtualenv venv` (si no funciona hay que instalar python 3.4, pip y virtualenv
	3. `source venv/bin/activate` (para entrar en el entorno virtual)
3. Instalar todas las dependencias; comprobar que no den errores
	1. `pip install -r requirements.txt`
4. Cambiar a una rama de feature. Esto es importante porque nos permitirá desarrollar libremente sin que lo que hay subido deje de funcionar.
	1. `git checkout feature/<nombre>`
5. Hacer las modificaciones necesarias
	1. Incluir nuevos tests y comprobar que los antiguos siguen funcionando
	Comprobar que todo funciona localmente.
		1. `python manager.py test`
	1. Subir los commits a la nueva rama y hacer una PR a la rama principal (master)


### Estructura de directorios

El directorio raíz del proyecto contiene los archivos de git, el project manager (`manager.py`) de Django, y los archivos de configuración de las dependencias del proyecto (`requirements.txt`) para PIP.

En la misma raíz hay, también, tres carpetas:
* __api/__ contiene los archivos generales de configuración del proyecto (`api.py`, `settings.py`, `urls.py`, `wsgi.py`), todos ellos requeridos por Django + TastyPie, y que determinan qué módulos habrá de ejecutar el proyecto y dónde se encuentran.
* __core/__ contiene clases, funciones y estructuras genéricas que no aportan nada fuera de contexto, pero que sirven de ayuda en distintos puntos del proyecto. Estas estructuras auxiliares están agrupadas en ficheros, según el servicio que proporcionen (por ejemplo, `authentication.py`, `models.py`, etc. ). Por lo demás, el formato es libre, a interpretación del desarrollador.
* __apps/__ contiene los módulos de que se compone el proyecto. Cada uno de estos módulos tiene su propio subdirectorio. En cada subdirectorio encontramos (potencialmente) los siguientes archivos:
	* `models.py`: Modelos de Django. Definen las entidades de la base de datos
	* `resources.py`: Recursos de TastyPie. Definen las entidades accesibles a través de la API
	* `authorizations.py`: Políticas de autorización a recursos de TastyPie
	* `factory.py`: Métodos que crean modelos dummy (para ayudar a crear datos de prueba)
	* `populate.py`: Archivo que se llama al ejecutar manage.py populate/resetdb, y que rellena la base de datos con datos de prueba
	* `tests.py`: Testing de Django y TastyPie
otros archivos auxiliares no estándares

_N.B. Existe una app (base) destinada a definir los modelos de datos secundarios (e.g. idioma, sectorDelMercado, etc.) y que contiene:_
* `enums.py`: Enumeraciones de valores discretos que puede tener un campo (e.g. Sexo={Masculino, Femenino, Otro})
* datos: Directorio con datos reales y consistentes con los que rellenar ciertos modelos auxiliares
* management: Directorio donde se definen comandos propios a ejecutar con manage.py, y que servirán de ayuda al desarrollar.
