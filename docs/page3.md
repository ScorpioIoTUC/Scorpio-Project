# Analisis de registros

[<- Atras ](/docs/page2.md)[/ Siguiente -> ](/docs/page4.md)

## Useful Commands

Despues de haber levantado la infraestructura
es posible poder ver los registros que cada servicio recibe, para ello puedes ingresar el siguiente comando en la terminal

```bash
make logs
```




## Quick Start

```bash
make start
```

The last command will build the docker stack  and the systemd service for the LoRa decoder. 



### Alternatives (Manual)
The last command `make start` does not allow you to view real-time logs from all containers from the docker stack while the service is being compiled. If you want to view the logs during compilation, you can run the following command in a separate terminal:

```bash 
docker compose -f deploy/docker-compose.yml up --build
```

After the docker stack is up, you can start the LoRa decoder service manually:

```bash
bash decoder/install_decoders.sh
```



Stop the stack keeping the volumes:

```bash
make stop
```
If you need to stop and remove all containers, volumes, and networks:

```bash
make delete-all
```

For more commands, execute the command `make help` to see the full list of available commands and their descriptions.

## Logs

Preview the logs of all services in real-time (docker stack)

```bash
make logs
```

Save them to a file (ordered by timestamp):

```bash
make save-logs
```

The result file will contain all logs from the services, and saved in the logs/ directory as *<timestamp>_all_containers.log*. 

Read Mosquitto’s file log:

```bash
docker compose -f deploy/docker-compose.yml exec mqtt sh -c 'tail -f /mosquitto/log/mosquitto.log'
```
