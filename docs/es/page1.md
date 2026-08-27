# 1. Hardware y preparación de la Raspberry Pi

[← Índice](README.md) | [Siguiente: SSH e instalación →](page2.md)

## Requisitos

- Raspberry Pi compatible y fuente de alimentación.
- Tarjeta microSD o SSD.
- Computador con [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
- Antena LNA y SDR.

<figure>
<img src="../imgs/materials.png" alt="Materiales necesarios para instalar la infraestructura de Scorpio">
<figcaption>Figura 1. Materiales necesarios para la instalación.</figcaption>
</figure>

Consulta la guía oficial [Getting Started de Raspberry Pi](https://www.raspberrypi.com/documentation/computers/getting-started.html) para el montaje físico.

## Configurar Raspberry Pi OS, Wi-Fi y SSH

En Raspberry Pi Imager<sup>1</sup>, selecciona el modelo, instala **Raspberry Pi OS (64-bit)** y elige la microSD o SSD. En la configuración avanzada:

1. Define el hostname, por ejemplo, `scorpio`.
2. Configura ubicación y zona horaria.
3. Crea el usuario y la contraseña para SSH.
4. Configura el SSID y la contraseña de la red Wi-Fi.
5. Activa SSH con autenticación por contraseña.

Pulsa **Write**, retira la unidad de forma segura, insértala en la Raspberry Pi y enciéndela.

<sup>1</sup> Sigue la guía oficial de Raspberry Pi para [instalar Raspberry Pi Imager](https://www.raspberrypi.com/documentation/computers/getting-started.html#imager-install) y preparar el medio de arranque.

## Montaje final

Conecta la Raspberry Pi a la red local mediante Ethernet y conecta la antena LNA al SDR.

<figure>
<img src="../imgs/final_arch.png" alt="Montaje final de la Raspberry Pi, el LNA y el SDR">
<figcaption>Figura 2. Montaje físico final de la infraestructura.</figcaption>
</figure>
