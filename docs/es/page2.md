# 2. Acceso por SSH e instalación de Scorpio CLI

[← Anterior](page1.md) | [Índice](README.md) | [Siguiente: Servicios →](page3.md)

## Conectarse por SSH

Con la Raspberry Pi encendida y en la misma red local, identifica su IP:

    arp -a

Conéctate con el usuario creado en Raspberry Pi Imager:

    ssh <usuario>@<direccion-ip>

## Instalar Scorpio CLI

Los sistemas basados en Debian protegen el entorno de Python del sistema. Instala Scorpio CLI con `pipx`, sin utilizar `sudo pip` ni `--break-system-packages`:

```bash
sudo apt update
sudo apt install -y pipx
pipx ensurepath
source ~/.profile
pipx install scorpio-cli
```

Si Scorpio CLI ya está instalado, actualízalo a la última versión:

```bash
pipx upgrade scorpio-cli
```

## Instalar las dependencias del sistema

Scorpio CLI descarga la última versión disponible de Scorpio-Project y ejecuta la instalación de dependencias:

```bash
scorpio setup
```

El proceso puede tardar varios minutos. Cuando finalice, reinicia la Raspberry Pi:

```bash
sudo reboot
```

Después del reinicio, vuelve a conectarte y prepara Docker:

```bash
ssh <usuario>@<direccion-ip>
scorpio setup-docker
```

El comando instala o verifica Docker, crea `.env` si no existe y levanta la infraestructura. La instalación termina cuando aparece `Infrastructure is up.`.
