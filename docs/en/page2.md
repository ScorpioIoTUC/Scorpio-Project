# 2. Installing Scorpio

[← Previous: local access](page1.md) | [Contents](README.md) | [Next: Tailscale →](page3.md)

> ⚠️ The local web interface is still under development. If you find an error, report it in [Issues](https://github.com/ScorpioIoTUC/Scorpio-Project/issues).

Scorpio can be installed through the web interface—the recommended option—or directly from the Raspberry Pi terminal.

## Option A: install through the web interface (recommended)

With this method, install Scorpio CLI on the computer used to administer the Raspberry Pi. The UI connects over SSH and runs the installation on the remote device.

### 1. Install Scorpio CLI

On macOS, create a virtual environment and install Scorpio CLI with `pip` or `pip3`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install scorpio-cli
# You can also use: pip3 install scorpio-cli
```

On Linux, install `pipx` with your distribution's package manager:

```bash
sudo apt update
sudo apt install -y pipx
pipx ensurepath
pipx install scorpio-cli
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install scorpio-cli
```

If Scorpio CLI is already installed, upgrade it using the same installation method:

```bash
# macOS or a virtual environment
pip install --upgrade scorpio-cli
# You can also use: pip3 install --upgrade scorpio-cli

# Linux with pipx
pipx upgrade scorpio-cli
```

### 2. Open the interface and connect to the Raspberry Pi

Run:

```bash
scorpio ui
```

The terminal will display:

```text
INFO:root:Server started at http://localhost:8000
```

Open [http://localhost:8000](http://localhost:8000) and enter the following information:

- **IP Address or hostname:** the Raspberry Pi hostname or IP address, such as `scorpio.local` or `192.168.1.100`.
- **Username:** the account created in Raspberry Pi Imager, such as `scorpio`.
- **Password:** the SSH password for that account.

The computer and Raspberry Pi must be reachable through the same local network or Tailscale. Click **Access** to start the SSH connection.

<figure>
<img src="../imgs/installation/scorpio-ui-ssh-login.png" alt="Scorpio web interface SSH connection form">
<figcaption>Figure 1. Entering the Raspberry Pi SSH credentials.</figcaption>
</figure>

### 3. Start the installation

After connecting, the main panel displays the **Ready to install** status. Make sure the Raspberry Pi has Internet access and enough free space, then click **Start installation**.

<figure>
<img src="../imgs/installation/scorpio-ui-install-ready.png" alt="Scorpio panel ready to start the installation">
<figcaption>Figure 2. Interface ready to start the installation.</figcaption>
</figure>

### 4. Monitor the installation

The interface downloads the latest Scorpio-Project release, installs the low-level dependencies, and configures the Docker infrastructure. This process can take several minutes and produces many events.

<figure>
<img src="../imgs/installation/scorpio-ui-install-logs.png" alt="Scorpio installation logs displayed in real time">
<figcaption>Figure 3. Installation in progress with real-time events.</figcaption>
</figure>

While the status is **Running**, do not close the interface or power off the Raspberry Pi. Click the `+` button for an event to view its details. If a problem occurs, the status changes to **Failed**, and the latest records help identify the cause. When it finishes successfully, the interface displays **Installation complete** with the **Completed** status.

### 5. Reboot the Raspberry Pi and manage services

After installation, the **Service status** card displays the infrastructure status and enables its controls.

<figure>
<img src="../imgs/installation/scorpio-ui-install-completed.png" alt="Scorpio installation completed with services stopped">
<figcaption>Figure 4. Installation completed and infrastructure controls available.</figcaption>
</figure>

Click **Reboot Raspberry Pi** to apply all system changes. The SSH connection closes temporarily. Wait a few minutes, reopen the interface, and enter the access credentials again.

The service controls work as follows:

- **Start:** starts the Scorpio Docker services.
- **Stop:** stops the services without deleting persistent data.
- **Refresh page:** requests the current status and reconnects the log display.
- **Restart services:** click **Stop**, wait for the status to change to **Stopped**, and then click **Start**.
- **Reboot Raspberry Pi:** restarts the entire operating system; it is not the same as restarting only the services.

When the infrastructure is active, its status changes to **Running**, and **Service logs** displays container events. You can filter the logs by service and time range.

<figure>
<img src="../imgs/installation/scorpio-ui-services.png" alt="Scorpio infrastructure service and log panel">
<figcaption>Figure 5. Running services and infrastructure logs.</figcaption>
</figure>

### 6. Configure the Station Key and API

After completing the installation, open **Settings** from the top navigation bar. Under **Station settings**, configure the connection used to publish Scorpio packets.

<figure>
<img src="../imgs/installation/scorpio-ui-station-settings.png" alt="Scorpio Station Key and API URL settings form">
<figcaption>Figure 6. Station Key and API base URL configuration.</figcaption>
</figure>

Complete the fields using the following format. For the production environment, use the API base URL shown below:

```text
Station Key:
a121183c-1f93-4675-8a6c-58e075022db4.tmQ0fJwNGsMZYPJpoBTYZq_JE9X1LPqQotmquA7vAvY

Scorpio API URL:
https://scorpio.cpsrtc.cl/api/
```

> **Important:** you must have an active Station Key to complete this configuration. The key is provided when you create the station on the [Scorpio platform](https://scorpio.cpsrtc.cl/). Copy and securely retain the key provided during that process; the value above is included only as a format example and does not provide access to any station. Never publish an active Station Key in documentation, repositories, screenshots, or messages.

In **Scorpio API URL**, enter the current production API address: `https://scorpio.cpsrtc.cl/api/`. Click **Save** to store the configuration. The interface updates the Raspberry Pi `.env` file and automatically restarts the `data-export` service.

If `Could not load Scorpio API settings` appears before installing Scorpio, complete the installation first and reopen **Settings**.

### 7. Check and install updates

Open **Updates** from the top navigation bar to check the installed Scorpio CLI and Scorpio-Project versions. If everything is current, the interface displays **Scorpio CLI is already up to date**.

<figure>
<img src="../imgs/installation/scorpio-ui-updates-current.png" alt="Scorpio updates page showing that the system is current">
<figcaption>Figure 7. Scorpio CLI and Scorpio-Project with no pending updates.</figcaption>
</figure>

Click **Check again** to repeat the check. If a newer version is available, the **Update** button appears.

<figure>
<img src="../imgs/installation/scorpio-ui-update-available.png" alt="Scorpio interface showing an available update">
<figcaption>Figure 8. Example of an available update.</figcaption>
</figure>

Click **Update** and keep the window open until the process finishes. Then return to the main panel and confirm that the infrastructure remains **Running**.

## Option B: install from the terminal

Connect to the Raspberry Pi over SSH and install Scorpio CLI with `pipx`:

```bash
sudo apt update
sudo apt install -y pipx
pipx ensurepath
source ~/.profile
pipx install scorpio-cli
```

If it is already installed:

```bash
pipx upgrade scorpio-cli
```

Verify the installation and run setup:

```bash
scorpio --help
scorpio setup
```

The command downloads the latest compatible release, runs `setup-host`, and prepares Docker with `setup-docker`. When it finishes, reboot and verify the services:

```bash
sudo reboot
# After reconnecting over SSH:
scorpio status
```

## Command reference

```text
scorpio ui             Start the setup web interface
scorpio setup          Install dependencies and configure Docker
scorpio setup-host     Install only the host dependencies
scorpio setup-docker   Configure only the Docker infrastructure
scorpio start          Build and start Scorpio services
scorpio stop           Stop services and preserve stored data
scorpio status         Show the current service status
scorpio logs           Follow service logs
scorpio build          Build the Docker images
scorpio reset          Stop services and permanently remove Docker data
scorpio connect2db     Connect to the Scorpio SQLite database
```

`scorpio reset` removes the volumes containing MQTT data, logs, and the SQLite database, so it requires explicit confirmation.

## Upgrade or uninstall Scorpio CLI

```bash
# macOS or a virtual environment
pip install --upgrade scorpio-cli
pip uninstall scorpio-cli

# Linux with pipx
pipx upgrade scorpio-cli
pipx uninstall scorpio-cli
```
