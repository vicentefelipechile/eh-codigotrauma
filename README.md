# Proyecto Codigo Trauma

*Este proyecto esta hecho para la asignatura de Arquitectura de DuocUC 2023*

## Pre-requisitos
- [Python 3.11+](https://www.python.org/downloads/)

---

## Descargar proyecto

Para descargar el proyecto es necesario clonar el repositorio actual, se puede realizar con el comando en consola:
```bash
git clone https://github.com/vicentefelipechile/eh-codigotrauma
```
Tambien es posible descargar el proyecto mediante la siguiente imagen:

![Sin título](https://github.com/vicentefelipechile/eh-codigotrauma/assets/70909800/0632b3fd-5828-44ce-afb8-d88ba06e41bb)

## Configurar proyecto

Antes de incializar el proyecto, es necesario configurar el archivo [config.json](https://github.com/vicentefelipechile/eh-codigotrauma/blob/main/root/config.json):
```bash
eh-codigotrauma/root/config.json
```

```
projectName            => Nombre del proyecto / Pagina
alwaysOpenBrowser      => El navegador siempre se abrira al iniciar el proyecto

DOMAIN_NAME            => Nombre que mostrara la pagina
DOMAIN_SHORTNAME       => Nombre alternativo que mostrara la pagina (Version corta)

backend                => Grupo de configuracion Backend
    DB_IP                => Direccion IP de la base de datos
    DB_PORT              => Puerto de la base de datos
    LANGUAGE_CODE        => Lenguaje principal de la pagina
    TIME_ZONE            => Zona horaria
    databaseRemota       => La base de datos sera remota o no
    modoDebug            => Modo desarrollador

API                    => Grupo de configuracion API
    Usuario              => Headers de los usuarios
    Emergencias          => Headers de las emergencias
```

## Inicializar proyecto

```bash

# Iniciar proyecto
python root

# Restaurar proyecto y generar datos ficticios
python root restaurar
python root generardatos
```

# Desarrollador

Para desarrollar este proyecto es necesario instalar requisitos los cuales estaran en el archivo (windows):
[Instalar Aplicaciones.bat](https://github.com/vicentefelipechile/eh-codigotrauma/blob/main/Instalar%20Aplicaciones.bat)
