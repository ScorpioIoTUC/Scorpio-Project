# 1. Materiales, instalación SO con Raspberry Image e infrastructura de red

[<- Atras ](/docs/README.md)[/ Siguiente -> ](/docs/page2.md)


# Requerimientos
## Materiales
<!-- Imagen con los materiales -->
![Imagen con materiales](/docs/imgs/materials.png)

Antes de instalar, debemos tener el software Raspberry Pi Imager instalado en el computador.
https://www.raspberrypi.com/software/. Además, se debe tener presenta una Rapsberry Pi, su fuente de alimentacion y una 
tarjeta MicroSD (o un disco duro SSD) para poder instalar el sistema operativo. Para las conexiones de los cables e inslatacion final de tu raspberry pi te recomendaos revisar la documentacion Getting Started de Raspberry Pi https://www.raspberrypi.com/documentation/computers/getting-started.html


## Configuracion del cuenta Wi-Fi y acceso SSH
Para este proceso debes crearte una cuenta para tu Raspberry Pi, 
https://www.raspberrypi.com/documentation/computers/getting-started.html
PAra este caso, te recomendamos seguir este tutorial en donde debes instalar Raspberry Pi imager, despues configurar tu dispositivo (tipo de rapsberry pi) y elegir el sistema oeprativo a utilizar, ene ste caos recomendamos el Raspberry pi OS 64-bit. Posteriormente debes seleccionar la unidad de almacenamiento, en este caso, debes tener conectada tu micro SD con su adaptador en tu computador. Finlamnete, debes configurar tu raspberry pi para que sea accesible en tu red local, en este caso debes primero
1. Configurar el hostname de tu raspberry pi, por ejemplo, **scorpio**.
2. Luego, defines la ubicacion y el time zone. 
3. Despues, debes crear una cuenta, en USer, definiendo el usuario y la contraseña. En este caso, es importante este paso para poder realizar la conexion SSH. 
4. PAra este tutroial, consideraremos la conexion mediante Wi-Fi, para ello, debes considerar la red local que vas a utilizar (SSID) y la contraseña. 
5. Finalmente, activa el uso de SSH, para ello, recomendamos utilizar tu contraseña como mecanismo de autenticacion. 
Ya con estas configuraciones, tu Raspbrery pi quedo lista para poder conectarse y como ultinmo paso debes escribir las configuracions, en Write Image dale opcion a Write. 

Ya completado el proceso debes retirar la tarjeta MicroSD de tu PC e insertarla en la ranura de la Raspberry Pi. 


## Infraestructura final
Una vez instalado el sistema operativo y realizada las configuraciones necesarias para las credenciales Wi-Fi, 
insertamos la tarjeta microSD a la raspberry pi. 

![Conexion final](/docs/imgs/final_arch.png)

Para este caso, utilizaremos un cabble ethernet conectado
directamente a la raspberry pi. 


<!-- Imagen con la infraestructura conectada -->
Al mismo tiempo, se debe conectar la LNA con el SDR. La infraestructura final debe quedar como en la imagen anterior.
