#!/bin/bash

# Abortar si hay errores
set -e

REBOOT_AFTER_INSTALL=1

log() {
    local level="$1"
    local step="$2"
    local step_id="$3"
    local message="$4"
    echo "log:${level}:${MODULE}:step:${step}/${TOTAL_STEPS}:${step_id}:${message}"
}

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
            echo "log:error:${MODULE}:step:0/${TOTAL_STEPS}:args:Argumento no reconocido: ${arg}"
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

log info 1 system_update "System update and upgrade started"
sudo apt-get update --yes
log info 1 system_update "System update and upgrade completed"
# sudo apt install rpi-usb-gadget -y
# sudo apt install --only-upgrade rpi-connect rpi-usb-gadget
# sudo rpi-usb-gadget on

# sudo apt-get full-upgrade -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"

log info 2 essential_dependencies "Essential dependencies installation started"
sudo apt-get install -y --no-install-recommends \
    curl build-essential cmake git pkg-config swig \
    python3-dev python3-pip python3-setuptools \
    python3-numpy python3-matplotlib python3-scipy
log info 2 essential_dependencies "Essential dependencies installation completed"


log info 3 gnuradio "GNU Radio installation started"
sudo apt-get install -y --install-recommends \
    gnuradio gnuradio-dev gr-osmosdr liborc-dev \
    libosmosdr-dev rtl-sdr libboost-all-dev
log info 3 gnuradio "GNU Radio installation completed"


log info 4 hardware_configuration "Hardware configuration started"

sudo usermod -aG plugdev $USER
sudo usermod -aG dialout $USER

sudo bash -c 'echo "blacklist dvb_usb_rtl28xxu" > /etc/modprobe.d/blacklist-rtl.conf'
sudo wget -q https://raw.githubusercontent.com/osmocom/rtl-sdr/master/rtl-sdr.rules -O /etc/udev/rules.d/20-rtlsdr.rules
log info 4 hardware_configuration "Hardware configuration completed"

log info 5 volk_optimization "VOLK optimization started"

VOLK_CONFIG="${HOME}/.volk/volk_config"

if ! command -v volk_profile >/dev/null 2>&1; then
    log warning 5 volk_optimization "volk_profile is not available; skipping optimization"
elif [ -f "$VOLK_CONFIG" ]; then
    log info 5 volk_optimization "VOLK is already optimized for this user"
    
else
    log info 5 volk_optimization "Profiling VOLK kernels. This may take several minutes"
    volk_profile
fi
log info 5 volk_optimization "VOLK optimization completed"


log info 6 gr_lora_sdr "GR-LoRa-SDR installation started"
if [ -d "gr-lora_sdr" ]; then 
    cd gr-lora_sdr
    log info 6 gr_lora_sdr "Repository already exists; pulling latest changes"
    git pull --ff-only
else
    log info 6 gr_lora_sdr "Cloning gr-lora_sdr repository"
    git clone https://github.com/tapparelj/gr-lora_sdr.git
    cd gr-lora_sdr
fi

mkdir -p build && cd build
cmake ..
make -j$(nproc)
sudo make install
sudo ldconfig
log info 6 gr_lora_sdr "GR-LoRa-SDR installation completed"

log info 7 tailscale "Tailscale installation started"
if command -v tailscale >/dev/null 2>&1; then
    log info 7 tailscale "Tailscale is already installed"
else
    curl -fsSL https://tailscale.com/install.sh | sh
fi

sudo systemctl enable --now tailscaled
tailscale version
log info 7 tailscale "Tailscale installation completed"

echo "log:info:${MODULE}:complete:installation_complete:Installation complete"

sync
if [ "$REBOOT_AFTER_INSTALL" -eq 1 ]; then
    echo "log:warning:${MODULE}:reboot:pending:Rebooting in 5 seconds"
    sleep 5
    sudo reboot
else
    echo "log:info:${MODULE}:reboot:skipped:No reboot requested"
    echo "log:warning:${MODULE}:reboot:recommended:Reboot manually before running Docker services"
fi