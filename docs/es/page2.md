# 2. Instalación de Scorpio

[← Anterior: acceso local](page1.md) | [Índice](README.md) | [Siguiente: Tailscale →](page3.md)

> ⚠️ La interfaz web local todavía está en desarrollo. Si encuentras un error, repórtalo en [Issues](https://github.com/ScorpioIoTUC/Scorpio-Project/issues).

Scorpio puede instalarse desde la interfaz web —la opción recomendada— o directamente desde la terminal de la Raspberry Pi.

## Opción A: instalar mediante la interfaz web (recomendado)

En este método, Scorpio CLI se instala en el computador desde el que administrarás la Raspberry Pi. La UI se conecta por SSH y ejecuta la instalación en el dispositivo remoto.

### 1. Instalar Scorpio CLI

En macOS, crea un entorno virtual e instala Scorpio CLI con `pip` o `pip3`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install scorpio-cli
# También puedes usar: pip3 install scorpio-cli
```

En Linux, se recomienda instalar `pipx` con el gestor de paquetes de la distribución:

```bash
sudo apt update
sudo apt install -y pipx
pipx ensurepath
pipx install scorpio-cli
```

En Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install scorpio-cli
```

Si Scorpio CLI ya está instalado, actualízalo según el método utilizado:

```bash
# macOS o entorno virtual
pip install --upgrade scorpio-cli
# También puedes usar: pip3 install --upgrade scorpio-cli

# Linux con pipx
pipx upgrade scorpio-cli
```

### 2. Abrir la UI e iniciar sesión

Ejecuta:

```bash
scorpio ui
```

El terminal mostrará:

```text
INFO:root:Server started at http://localhost:8000
```

Abre [http://localhost:8000](http://localhost:8000) e ingresa el hostname o dirección IP, usuario y contraseña SSH de la Raspberry Pi. Ambos dispositivos deben estar accesibles desde la misma red o mediante Tailscale.

<figure>
<img src="../imgs/installation/scorpio-ui-ssh-login.png" alt="Formulario de conexión SSH de la interfaz web de Scorpio">
<figcaption>Figura 1. Inicio de sesión SSH en la Raspberry Pi.</figcaption>
</figure>

### 3. Iniciar la instalación

Después de conectarte aparecerá el panel de instalación. Verifica que la Raspberry Pi tenga conexión a Internet y espacio disponible, y haz clic en **Iniciar instalación**.

<figure>
<img src="../imgs/installation/scorpio-ui-install-ready.png" alt="Panel de Scorpio listo para iniciar la instalación">
<figcaption>Figura 2. Panel listo para iniciar la instalación.</figcaption>
</figure>

La UI descarga el último release de Scorpio-Project, instala las dependencias del host y prepara la infraestructura Docker. El proceso puede tardar varios minutos y genera una gran cantidad de logs.

<figure>
<img src="../imgs/installation/scorpio-ui-install-logs.png" alt="Logs de instalación de Scorpio mostrados en tiempo real">
<figcaption>Figura 3. Progreso y logs de instalación en tiempo real.</figcaption>
</figure>

Revisa los logs durante la instalación. Si ocurre un problema, el estado cambiará a **Failed** y el último registro indicará la causa. Cuando el proceso finalice correctamente, aparecerá **Completed**.

### 4. Reiniciar y administrar los servicios

Después de completar la instalación, se recomienda usar el botón **Reiniciar Raspberry Pi**. La conexión se cerrará temporalmente; espera unos minutos y vuelve a iniciar sesión cuando el dispositivo esté disponible.

La UI mostrará el estado de la infraestructura, los logs de los servicios y los controles **Start** y **Stop**. Usa **Update page** para volver a consultar el estado y reconectar los logs cuando sea necesario.

<figure>
<img src="../imgs/installation/scorpio-ui-services.png" alt="Panel de servicios y logs de infraestructura de Scorpio">
<figcaption>Figura 4. Administración de la infraestructura y logs de servicios.</figcaption>
</figure>

## Opción B: instalar desde la terminal

Conéctate por SSH a la Raspberry Pi e instala Scorpio CLI con `pipx`:

```bash
sudo apt update
sudo apt install -y pipx
pipx ensurepath
source ~/.profile
pipx install scorpio-cli
```

Si ya está instalado:

```bash
pipx upgrade scorpio-cli
```

Comprueba la instalación y ejecuta el setup:

```bash
scorpio --help
scorpio setup
```

El comando descarga el último release compatible, ejecuta `setup-host` y prepara Docker con `setup-docker`. Cuando termine, reinicia y verifica los servicios:

```bash
sudo reboot
# Después de volver a conectarte por SSH:
scorpio status
```

## Referencia de comandos

```text
scorpio ui             Inicia la interfaz web de configuración
scorpio setup          Instala las dependencias y configura Docker
scorpio setup-host     Instala únicamente las dependencias del host
scorpio setup-docker   Configura únicamente la infraestructura Docker
scorpio start          Construye e inicia los servicios de Scorpio
scorpio stop           Detiene los servicios y conserva los datos
scorpio status         Muestra el estado de los servicios
scorpio logs           Sigue los registros de los servicios
scorpio build          Construye las imágenes Docker
scorpio reset          Detiene los servicios y elimina permanentemente sus datos
scorpio connect2db     Abre una conexión con la base de datos SQLite de Scorpio
```

`scorpio reset` elimina los volúmenes con los datos MQTT, los registros y la base de datos SQLite, por lo que exige una confirmación explícita.

## Actualizar o desinstalar Scorpio CLI

```bash
# macOS o entorno virtual
pip install --upgrade scorpio-cli
pip uninstall scorpio-cli

# Linux con pipx
pipx upgrade scorpio-cli
pipx uninstall scorpio-cli
```
