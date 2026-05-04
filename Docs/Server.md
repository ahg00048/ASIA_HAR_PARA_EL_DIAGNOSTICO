# Aplicación de servidor
---
## STACK utilizado

- Python 3.12.4
- DJango
- DJango Rest Framework
- MySQL 9.7

Las dependencias del proyecto se pueden encontrar en el fichero "requirements.txt" del directorio.

---

## Desarrollo

Antes de comenzar, hay que mencionar que por la inexperiencia en el desarrollo de proyectos software con el lenguaje y los marcos de desarrollo utilizados, no se ha podido implementar muchas funcionalidades con la robustez deseada, al menos de momento. 

#### Estructura

En el directorio del projecto (el directorio "server") podemos encontrar 3 elementos importantes:

- __ASIA_HAR_SERVER__: Aquí se encuentran la configuración general de la aplicación (`settings.py`) y la base de las URIs de la API (`urls.py`).
<br>
- __ASIA_HAR_CORE__: Aquí se encuentra la logíca interna de la aplicación, la creación de modelos, vistas (en nuestro caso los 'endpoints' de la API), serializadores, etc. 
<br>
- __manage.&#8204;py:__: Script the la aplicación para toda su administración.

#### Implementado

Lo poco desarrollado se trata de un sistema básico compuesto por usuarios y sus pacientes, los cuales tienen asignados datos de sensores. 

El sistema creado requiere de modificaciones para implementar autorización y autenticación apropiadadas, seguridad y restricciones, sin embargo debido a la falta de tiempo, solo se ha tomado como prioridad un sistema funcional.

Las funcionalidades implementadas se han probado y verificado que su comportamiento es correcto. 

- Se puede registrar, modificar, eliminar y obtener usuarios. 
- Se pueden añadir, eliminar y obtener pacientes de dichos usuarios.
- Se ha creado un 'endpoint' a modo de prueba para devolver unos datasets de ejemplo comprimidos en un zip para así empezar con el desarrollo de la aplicación de escritorio, ya que al no disponer de la información necesaria sobre la comunicación con un nodo niebla (raspberry PI), ni un ejemplar para realizar pruebas, no se ha podido implementar dicha funcionalidad.

#### Uso de Manage.&#8204;py 

Con el objetivo de correr el servidor, crear los esquemas de la base de datos, migrarlos y crear usuarios que tengan acceso administrativo de la API, tenemos los siguientes comandos respectivamente:

Activar el servidor:
```
py manage.py runserver
```
Crear migraciones / esquema
```
py manage.py makemigrations
```
Realizar migración
```
py manage.py migrate
```
Crear super usuario con acceso administrativo a la API desde la url "admin/"
```
py manage.py createsuperuser
```