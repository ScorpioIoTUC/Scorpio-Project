#!/bin/bash

# Abortar si hay errores
set -e

REBOOT_AFTER_INSTALL=1

for arg in "$@"; do
    case "$arg" in
        --no-reboot)
            REBOOT_AFTER_INSTALL=0
            ;;
        --help|-h)
            echo "Uso: $0 [--no-reboot]"
            exit 0
            ;;
        *)
            echo "Argumento no reconocido: $arg"
            echo "Uso: $0 [--no-reboot]"
            exit 1
            ;;
    esac
done

export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a

TARGET_DIR="${HOME}"
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

echo "--- 1/6 System update and upgrade ---"
sudo apt-get update --yes
# sudo apt install rpi-usb-gadget -y
# sudo apt install --only-upgrade rpi-connect rpi-usb-gadget
# sudo rpi-usb-gadget on

# sudo apt-get full-upgrade -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"

echo "--- 2/6 Essential dependencies ---"
sudo apt-get install -y --no-install-recommends \
    build-essential cmake git pkg-config swig \
    python3-dev python3-pip python3-setuptools \
    python3-numpy python3-matplotlib python3-scipy

echo "--- 3/6 GNU Radio installation ---"
sudo apt-get install -y --install-recommends \
    gnuradio gnuradio-dev gr-osmosdr liborc-dev \
    libosmosdr-dev rtl-sdr libboost-all-dev

echo "--- 4/6 Hardware configuration ---"
sudo usermod -aG plugdev $USER
sudo usermod -aG dialout $USER

sudo bash -c 'echo "blacklist dvb_usb_rtl28xxu" > /etc/modprobe.d/blacklist-rtl.conf'
sudo wget -q https://raw.githubusercontent.com/osmocom/rtl-sdr/master/rtl-sdr.rules -O /etc/udev/rules.d/20-rtlsdr.rules

echo "--- 5/6 Volk optimization ---"
volk_profile

echo "--- 6/6 GR-LoRa-SDR installation ---"
if [ -d "gr-lora_sdr" ]; then 
    cd gr-lora_sdr
    git pull --ff-only
else
    git clone https://github.com/tapparelj/gr-lora_sdr.git
    cd gr-lora_sdr
fi

mkdir -p build && cd build
cmake ..
make -j$(nproc)
sudo make install
sudo ldconfig

echo "--- Installation complete! ---"
sync
if [ "$REBOOT_AFTER_INSTALL" -eq 1 ]; then
    echo "Rebooting in 5 seconds..."
    sleep 5
    sudo reboot
else
    echo "No reboot requested (--no-reboot)."
    echo "Recommended: reboot manually before running Docker services."
fi