# Backlog Scrum API

_API Rest para dar servicio a Backlog Scrum en el marco de la materia CI4712_

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **Deployment** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

_**Python3**_
```
sudo apt update
sudo apt install software-# Backlog Scrum API

_API Rest para dar servicio a Backlog Scrum en el marco de la materia CI4712_

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **Deployment** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

_**Python3**_
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3
```

_**sqlite3**_
```
sudo apt update
sudo apt-get install sqlite3
```

**virtualenv**

_instala el entorno virtual con_
```
pip install virtualenv
```

_crea un directorio para alojarlo con_
```
mkdir virtualenvs
cd virtualenvs
```

_instala el entorno_
```
virtualenv env
```

_para activarlo utiliza_
```
source env/bin/activate
```

_para desactivarlo utiliza_
```
source env/bin/deactivate
```

### Instalación 🔧

_Sigue estos pasos una vez superados los **Pre-requisitos**:_

_**NOTA: manten activado el entorno virtual para estas instalaciones.**

_clona el repositorio de github_

```
git clone enlace_del_repositorio
```

_Fue generado un file de requerimientos que permitira la instalacion automatica de los modulos con_

```
pip install requirements.txt
```

_SQLite permite tener una base de datos "portatil" de modo que ya vendra incluida en el repositorio._


## Sobre corrida, coding de la aplicacion ⌨️

### Estructura de framework

_Se creo un filesystem con ciertos aspectos que faciliten la organizacion de los diversos modelos necesarios._

#### apps
_en este directorio reposaran las diversas entidades de la base de dato bajo el nombre de **app**._
_Los directorios de las mismas contendran dos files: **models.py** y **services.py**._
_el primero contendra los tipajes de las columnas que conformaran la tabla que modela nuestra entidad y el serializador._
_el segundo contendra la funcion que procesara los datos a retornar al usuario en lso servicios._

**NOTA: anexe una app denominada "example_app" donde pueden leer como crear los servicios. Importante recordar la creacion de __init__.py en cada directorio**

#### database
_aqui reposara el archivo de **SQLite**._

#### migrations
_reservado del sistema, se autogeneraran en cada migracion y actualizacion de la base de datos **SQLite**._

#### settings
_en este directorio se aloja el file **environment.py** el cual contiene algunas variables globales que marcan la raiz del proyecto, la ruta de la base de datos y el seteo del tipo de configuracion a usar(development de momento)._

#### app.py, config.py, manage.py
_files en la raiz que inicializan nuestro api._

### Comandos importantes

_para correr servidor local en **127.0.0.1:5000**_
```
python manage.py runserver
```

_para inicializar base de datos **SOLO USAR CUANDO CREAN UNA BASE NUEVA**_
```
python manage.py db init                                                                                                  
```

_para crear migracion **USAR CADA VEZ QUE GENERAN O MODIFICAN UNA TABLA**_
```
python manage.py db migrate                                                                                                  
```

_para actualizar base de datos **USAR DESPUES DE CREAR MIGRACIONES**_
```
python manage.py db upgrade                                                                                                  
```

## Ejemplos de servicios de example_app

_para agregar un libro a base de datos._
```
http://127.0.0.1:5000/add?name=Quijote&author=Cervantes Miguel&published=1605
```

_para obtener el libro agregado por su id._
```
http://127.0.0.1:5000/get/1
```

_para obtener todos los libros agregados._
```
http://127.0.0.1:5000/getall
```


## Despliegue 📦

_Por definir_

## Construido con 🛠️

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - El framework web usado
* [SQLite](https://www.sqlite.org/index.html) - relational database management system
