# 2. Acceso por SSH e instalación de dependencias

[← Anterior](page1.md) | [Índice](README.md) | [Siguiente: Servicios →](page3.md)

## Conectarse por SSH

Con la Raspberry Pi encendida y en la misma red local, identifica su IP:

    arp -a

Conéctate con el usuario creado en Raspberry Pi Imager:

    ssh <usuario>@<direccion-ip>

## Instalar Scorpio

    git clone https://github.com/ScorpioIoTUC/Scorpio-Project.git
    cd Scorpio-Project
    make setup-all

El proceso puede tardar entre tres y cinco minutos. Cuando finalice, reinicia:

    sudo reboot

Después del reinicio, vuelve a conectarte y prepara Docker:

    ssh <usuario>@<direccion-ip>
    cd Scorpio-Project
    make setup-docker

El comando crea `.env` si no existe y levanta la infraestructura Docker. Completa sus variables antes de enviar datos al servidor. La instalación termina cuando aparece `Infrastructure is up.`.
