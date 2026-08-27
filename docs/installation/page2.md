# Conexion a traves de SSH a la Raspberry PI e instalacion de dependencias

## Conexion a SSH
Ahora deben buscar la configuracion del raspberry pi actualmente conectado por ethernet en la red wi-fi que
se encuentran conectados. Una vez creada la configuracionde red, debemos acceder a la raspberry pi a traves de ssh. 

En primer lugar, deben buscar la direccion IP donde se encuentra conectada la raspberry pi en su red local, para ello pueden realizar 
```bash
 arp -a
```
para listar todas las direcciones IP disponibles.
```bash
ssh <user>@<ip-address>
```
En este caso deben agregar como prefijo el nombre del usuario que configuraron en la instlacion con Raspberry Pi Imager, y el ip-adress es la direccion ip donde se eneucntra actualmente la raspberry pi en su red local. 

Luego, en el CLI les pedira la contraseñ aconfigurada previamente. 

## Instalacion de Scorpio
Ya cuando estes en la CLI, debes importar el paquete del repositorio con git clone
```bash
git clone https://github.com/ScorpioIoTUC/Scorpio-Project.git
```

Una vez importado, debes dirigirte a este repositorio, 
```bash 
cd Scorpio-Project
```

Ahora que estas dentro del repositorio, debes instalar las dependencias de librerias, para ello ejecuta el siguiente comando. Este comando instala todas las dependencias utilizadas de Scorpio. El tiempo toma entre 3 a 5 minutos. 

```bash
make setup-all
```

Ya cuando haya terminado la instalacion, te aparecerá el mensaje 
```bash 
--- Installation complete! ---
No reboot requested (--no-reboot).
Recommended: reboot manually before running Docker services.
make[1]: Leaving directory '/home/scorpio/Scorpio-Project'

After login, run: make setup-docker
```

Esto indica que las dependencias fueron ya instaladas, para aplicarlas, debes hacer reboot del sistema
```bash
sudo reboot
```
lo que reseteará la raspberry pi por unos minutos para poder configurar las nuevas dependencias del sistema. Luego debes conectarte nuevamente por SSH exactamente igual como lo hiciste en el paso [Conexion a SSH](#conexion-a-ssh), y dirigirte a la carpeta de Scorpio-Project

```bash
ssh <user>@<ip-address>
cd Scorpio-Project
```

Posteriormente, debes realizar 

```bash
make setup-docker
```
```bash
scorpio@scorpio:~/Scorpio-Project$ make setup-docker
[setup-docker] Created .env; replace <API_URL> and <KEY> before sending data
bash ./scripts/bootstrap.sh --docker-only
[docker] Preparing Docker environment...

```
este comando levatnara toda la infraestructura de docker, y los servicios respectivos, al mismo tiempo 
creará si no existe un archivo de variables de ambiente **.env**  que contiene las sigueintes variables
```.env


```


Una vez la infraestrucutra esta levantada, te apaarecerán todos los servicios levantados de docker
```bash
[+] up 11/11
 ✔ Image deploy-data_ingest     Built                                                                                               75.7s
 ✔ Image deploy-data_preprocess Built                                                                                               75.7s
 ✔ Image deploy-data_storage    Built                                                                                               75.7s
 ✔ Image deploy-data_clean      Built                                                                                               75.7s
 ✔ Image deploy-data_export     Built                                                                                               75.7s
 ✔ Container mqtt-broker        Started                                                                                              4.6s
 ✔ Container data-preprocess    Started                                                                                              4.6s
 ✔ Container data-ingest        Started                                                                                              7.9s
 ✔ Container data-storage       Started                                                                                              4.9s
 ✔ Container data-clean         Started                                                                                              6.8s
 ✔ Container data-export        Started                                                                                              6.9s
NAME              IMAGE                    COMMAND                  SERVICE           CREATED          STATUS                  PORTS
data-clean        deploy-data_clean        "python -m src.entry…"   data_clean        7 seconds ago    Up Less than a second
data-export       deploy-data_export       "python -m src.entry…"   data_export       7 seconds ago    Up Less than a second
data-ingest       deploy-data_ingest       "python -m src.entry…"   data_ingest       8 seconds ago    Up Less than a second
data-preprocess   deploy-data_preprocess   "python -m src.entry…"   data_preprocess   8 seconds ago    Up 3 seconds
data-storage      deploy-data_storage      "python -m src.entry…"   data_storage      8 seconds ago    Up 3 seconds
mqtt-broker       eclipse-mosquitto:2      "/docker-entrypoint.…"   mqtt              10 seconds ago   Up 5 seconds            0.0.0.0:1883->1883/tcp, [::]:1883->1883/tcp
[docker] Infrastructure is up.
```



