# 3. Ejecución y monitoreo con Scorpio CLI

[← Anterior](page2.md) | [Índice](README.md) | [Siguiente: Scorpio Developers →](page4.md)

Scorpio CLI centraliza la instalación, ejecución y administración de la infraestructura local.

## Comandos disponibles

```text
scorpio ui             Inicia la interfaz de configuración
scorpio setup          Instala las dependencias del sistema
scorpio setup-docker   Configura e inicia la infraestructura Docker
scorpio start          Inicia los servicios de Scorpio
scorpio stop           Detiene los servicios y conserva los datos
scorpio status         Muestra el estado de los servicios
scorpio logs           Muestra los registros en tiempo real
scorpio build          Construye las imágenes Docker
scorpio reset          Detiene los servicios y elimina permanentemente sus datos
```

## Operación habitual

Inicia los servicios:

```bash
scorpio start
```

Consulta su estado o sigue sus registros:

```bash
scorpio status
scorpio logs
```

Detén los servicios sin eliminar los datos persistentes:

```bash
scorpio stop
```

`scorpio reset` elimina los volúmenes de Docker que contienen los datos MQTT, los registros y la base de datos SQLite. Por seguridad, requiere una confirmación explícita.

## Actualizar o desinstalar Scorpio CLI

```bash
pipx upgrade scorpio-cli
pipx uninstall scorpio-cli
```
