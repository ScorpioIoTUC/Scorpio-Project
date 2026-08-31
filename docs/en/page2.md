# 2. SSH access and Scorpio CLI installation

[← Previous](page1.md) | [Contents](README.md) | [Next: Services →](page3.md)

## Connect over SSH

With the Raspberry Pi powered on and connected to the same local network, identify its IP address:

    arp -a

Connect with the user created in Raspberry Pi Imager:

    ssh <username>@<ip-address>

## Install Scorpio CLI

Debian-based systems protect the system Python environment. Install Scorpio CLI with `pipx` instead of using `sudo pip` or `--break-system-packages`:

```bash
sudo apt update
sudo apt install -y pipx
pipx ensurepath
source ~/.profile
pipx install scorpio-cli
```

If Scorpio CLI is already installed, upgrade it to the latest version:

```bash
pipx upgrade scorpio-cli
```

## Install system dependencies

Scorpio CLI downloads the latest available Scorpio-Project release and installs its dependencies:

```bash
scorpio setup
```

The process may take several minutes. When it finishes, reboot the Raspberry Pi:

```bash
sudo reboot
```

After the reboot, reconnect and prepare Docker:

```bash
ssh <username>@<ip-address>
scorpio setup-docker
```

This command installs or checks Docker, creates `.env` if it does not exist, and starts the infrastructure. Installation is complete when `Infrastructure is up.` appears.
