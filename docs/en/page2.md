# 2. SSH access and dependency installation

[← Previous](page1.md) | [Contents](README.md) | [Next: Services →](page3.md)

## Connect over SSH

With the Raspberry Pi powered on and connected to the same local network, identify its IP address:

    arp -a

Connect with the user created in Raspberry Pi Imager:

    ssh <username>@<ip-address>

## Install Scorpio

    git clone https://github.com/ScorpioIoTUC/Scorpio-Project.git
    cd Scorpio-Project
    make setup-all

The process may take three to five minutes. When it finishes, reboot:

    sudo reboot

After the reboot, reconnect and prepare Docker:

    ssh <username>@<ip-address>
    cd Scorpio-Project
    make setup-docker

This command creates `.env` if it does not exist and starts the Docker infrastructure. Complete its variables before sending data to the server. Installation is complete when `Infrastructure is up.` appears.
