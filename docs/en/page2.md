# 2. Scorpio CLI installation

[← Previous: local access](page1.md) | [Contents](README.md) | [Next: Tailscale →](page3.md)

Run this stage on the Raspberry Pi after connecting over SSH.

## Install Scorpio CLI

Debian-based systems protect the system Python environment. Therefore, install Scorpio CLI with `pipx` without using `sudo pip` or `--break-system-packages`.

```bash
sudo apt update
sudo apt install -y pipx
pipx ensurepath
source ~/.profile
pipx install scorpio-cli
```

A successful installation displays output similar to the following. The version numbers may differ:

```text
installed package scorpio-cli <version>, installed using Python <version>
These apps are now globally available
  - scorpio
done!
```

If Scorpio CLI is already installed, upgrade it instead of reinstalling it:

```bash
pipx upgrade scorpio-cli
```

Check that the command is available:

```bash
scorpio --help
```

## Install Scorpio

The following step is required. Scorpio CLI downloads the latest compatible Scorpio-Project release, installs the low-level dependencies, and configures the Docker infrastructure.

```bash
scorpio setup
```

The process may take several minutes. It completes successfully when the terminal reports that the infrastructure is running.

<figure>
<img src="../imgs/installation/scorpio-infrastructure-ready.png" alt="Terminal showing that the Scorpio Docker infrastructure is running">
<figcaption>Figure 1. Scorpio installed and the Docker infrastructure started successfully.</figcaption>
</figure>

You do not need to run `scorpio setup-docker` after a successful installation with `scorpio setup`.

## Reboot and verify

Reboot the Raspberry Pi to apply group, device, and service changes:

```bash
sudo reboot
```

The SSH connection will close. Wait for the device to boot, reconnect, and verify the services:

```bash
ssh <username>@<ip-address>
scorpio status
```

The reboot also activates the user's permission to communicate with Docker. Running `scorpio status` before rebooting may report `permission denied while trying to connect to the Docker daemon socket`.

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

Use `scorpio --help` to display the general help. The `scorpio setup-docker` command remains available to reinstall or repair only the Docker layer; it is not part of the normal flow described above.

The `scorpio reset` command removes the volumes containing MQTT data, logs, and the SQLite database, so it requires explicit confirmation.

## Upgrade or uninstall Scorpio CLI

```bash
pipx upgrade scorpio-cli
pipx uninstall scorpio-cli
```
