# 3. Remote access with Tailscale

[← Previous: Scorpio CLI](page2.md) | [Contents](README.md) | [Next: Scorpio Developers →](page4.md)

Tailscale creates a private network between the Raspberry Pi and your devices. It lets you connect over SSH from outside the local network without opening router ports.

## Enable Tailscale on the Raspberry Pi

`scorpio setup` installs Tailscale and starts its service. Verify the installation:

```bash
tailscale version
sudo systemctl status tailscaled
```

Press `q` to exit the service view. Then link the Raspberry Pi to your account:

```bash
sudo tailscale up
```

The command displays a one-time authentication URL:

```text
To authenticate, visit:

    https://login.tailscale.com/a/...
```

Open the link, sign in to Tailscale, and authorize the device. The terminal displays `Success.` when linking is complete.

## Get the Tailscale IP address

Check the status and the IPv4 address assigned to the Raspberry Pi in its terminal:

```bash
tailscale status
tailscale ip -4
```

The address has a format similar to `100.x.y.z`. Do not use a documentation example as the device's actual address.

## Prepare the client computer

Install the [Tailscale application](https://tailscale.com/docs/install) on the computer you will connect from and sign in with an account that has access to the same Tailscale network.

If the application is already installed and connected, you do not need to reinstall Tailscale or run another terminal installer.

## Connect over SSH through Tailscale

**With Tailscale active on both devices**, run the following command from the client computer:

```bash
ssh <username>@<raspberry-tailscale-ip>
```

For example:

```bash
ssh scorpio@100.x.y.z
```


<figure>
<img src="../imgs/installation/tailscale-status.png"alt="Terminal showing that the Scorpio Docker infrastructure is running">
<figcaption>Figure 1. Example of the Tailscale application on Mac OS. To connect using Tailscale, it must always be active</figcaption>
</figure>

Once the SSH connection has been established, you can run commands on the Raspberry Pi as if you were sitting in front of it.

## Recommendations for using Tailscale

If the Tailscale command is available on the client, you can test connectivity first:

```bash
tailscale ping <raspberry-tailscale-ip>
```

Running `tailscale ping` against that address from the Raspberry Pi itself displays `is local Tailscale IP`. This is expected, but it does not test the connection from the client computer.

The first SSH connection may display a host authenticity warning. Compare the displayed fingerprint with the Raspberry Pi fingerprint:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

If they match, answer `yes`. If the same Raspberry Pi was already known through its local IP address, SSH may also report that the key is associated with another address. This is expected when it is the same device.

<!-- ## Quick troubleshooting

```bash
tailscale status
sudo systemctl restart tailscaled
sudo tailscale up
```

If the Raspberry Pi does not appear in the application, confirm that both devices have Internet access and belong to the same Tailscale network. -->
