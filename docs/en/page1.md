# 1. Raspberry Pi OS installation and local access

[← Contents](README.md) | [Next: Scorpio CLI installation →](page2.md)

## Requirements

- Compatible Raspberry Pi and power supply.
- microSD card or SSD.
- Computer with [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
- Connection to the same local network that the Raspberry Pi will use.
- Antenna, LNA amplifier, and SDR receiver for the final assembly.

<figure>
<img src="../imgs/materials.png" alt="Materials required to install the Scorpio infrastructure">
<figcaption>Figure 1. Materials required for installation.</figcaption>
</figure>

## Prepare the boot media

Open Raspberry Pi Imager<sup>1</sup> and complete the following steps. The screenshots use a Raspberry Pi 4 as an example.

### 1. Select the Raspberry Pi

Choose the exact model you will use.

<figure>
<img src="../imgs/installation/rpi-imager-select-device.png" alt="Selecting Raspberry Pi 4 in Raspberry Pi Imager">
<figcaption>Figure 2. Device selection.</figcaption>
</figure>

### 2. Select the operating system

Select **Raspberry Pi OS (64-bit)**.

<figure>
<img src="../imgs/installation/rpi-imager-select-os.png" alt="Selecting 64-bit Raspberry Pi OS">
<figcaption>Figure 3. Operating system selection.</figcaption>
</figure>

### 3. Select the storage device

Choose the microSD card or SSD where the system will be installed.

> **Warning:** this process erases all data on the selected device. Check its name and capacity before continuing.

<figure>
<img src="../imgs/installation/rpi-imager-select-storage.png" alt="Selecting a storage device in Raspberry Pi Imager">
<figcaption>Figure 4. Storage device selection.</figcaption>
</figure>

### 4. Set the hostname

Use a recognizable name, such as `scorpio`. If the network supports mDNS, you will later be able to connect through `scorpio.local`.

<figure>
<img src="../imgs/installation/rpi-imager-hostname.png" alt="Setting the scorpio hostname">
<figcaption>Figure 5. Hostname configuration.</figcaption>
</figure>

### 5. Configure localization

Select the appropriate country, time zone, and keyboard layout.

<figure>
<img src="../imgs/installation/rpi-imager-localisation.png" alt="Country and time zone configuration">
<figcaption>Figure 6. Localization settings.</figcaption>
</figure>

### 6. Create the user

Set a username and a strong password. These credentials will be used later to connect over SSH.

<figure>
<img src="../imgs/installation/rpi-imager-user.png" alt="Creating the scorpio user in Raspberry Pi Imager">
<figcaption>Figure 7. User creation.</figcaption>
</figure>

### 7. Configure Wi-Fi

Enter the network name, password, and country.

<figure>
<img src="../imgs/installation/rpi-imager-wifi.png" alt="Wi-Fi network configuration">
<figcaption>Figure 8. Wi-Fi configuration.</figcaption>
</figure>

### 8. Enable SSH

Enable **Enable SSH**. To reproduce the configuration shown here, select password authentication.

<figure>
<img src="../imgs/installation/rpi-imager-ssh.png" alt="Enabling SSH with password authentication">
<figcaption>Figure 9. SSH remote access configuration.</figcaption>
</figure>

### 9. Write the image

Review the settings and click **Write**. When the process finishes, safely remove the device, insert it into the Raspberry Pi, and power it on.

<figure>
<img src="../imgs/installation/rpi-imager-writing.png" alt="Writing Raspberry Pi OS to the selected device">
<figcaption>Figure 10. Writing the operating system.</figcaption>
</figure>

<sup>1</sup> We recommend following Raspberry Pi's official guide to [install and use Raspberry Pi Imager](https://www.raspberrypi.com/documentation/computers/getting-started.html#imager-install).

## Final assembly

Connect the SDR to a Raspberry Pi USB port, then connect the antenna to the SDR through the LNA amplifier.

<figure>
<img src="../imgs/final_arch.png" alt="Final Raspberry Pi, LNA, and SDR assembly">
<figcaption>Figure 11. Final physical infrastructure assembly.</figcaption>
</figure>


## Find the Raspberry Pi on the local network

Wait a few minutes for the Raspberry Pi to boot. The computer and Raspberry Pi must be connected to the same network.

First, try the hostname configured earlier:

```bash
ping scorpio.local
```

Stop the command with `Ctrl+C`. If it responds, connect directly with `ssh scorpio@scorpio.local`.

If the hostname does not respond and you already know the IP address, skip the scan. Otherwise, install `nmap` on your computer and scan the local subnet. Replace `192.168.1.0/24` if your network uses a different range.

On macOS:

```bash
brew install nmap
```

On Debian or Ubuntu:

```bash
sudo apt update
sudo apt install -y nmap
```

Run the scan:

```bash
sudo nmap -sn 192.168.1.0/24 | grep -B 2 -i "Raspberry"
```

Example output:

```text
Nmap scan report for 192.168.1.100
Host is up (0.018s latency).
MAC Address: DC:A6:32:XX:XX:XX (Raspberry Pi Trading)
```

Pinging the broadcast address may help refresh the local device table, but not every device will reply:

```bash
ping 192.168.1.255
```

## Connect over SSH

Use the account created in Raspberry Pi Imager and the IP address you found:

```bash
ssh <username>@<ip-address>
```

For example:

```bash
ssh scorpio@192.168.1.100
```

On the first connection, SSH asks you to confirm the device identity. Verify the fingerprint when available, answer `yes`, and enter the configured password.

