#!/bin/bash

# Abortar si hay errores
set -e

# --- CONFIGURACIÓN DE RUTA ---
# Esto asegura que el script trabaje en /home/scorpio sin importar desde donde lo ejecutes
TARGET_DIR="/home/scorpio"
cd "$TARGET_DIR"

echo "--- 1/6 System update and upgrade ---"
sudo apt update && sudo apt full-upgrade -y

echo "--- 2/6 Essential dependencies ---"
sudo apt install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    swig \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-numpy \
    python3-matplotlib \
    python3-scipy

echo "--- 3/6 GNU Radio installation ---"
sudo apt-get install -y \
    gnuradio \
    gnuradio-dev \
    gr-osmosdr \
    liborc-dev \
    libosmosdr-dev \
    rtl-sdr

echo "--- 4/6 Hardware configuration for USB ---"
sudo usermod -aG plugdev $USER
sudo usermod -aG dialout $USER
echo "Done!"

echo "--- 5/6 Volk optimization ---"
# Esto puede tardar varios minutos
volk_profile

echo "--- 6/6 GR-LoRa-SDR installation ---"
# Borramos si ya existe para una instalación limpia
if [ -d "gr-lora_sdr" ]; then 
    sudo rm -rf gr-lora_sdr 
fi

git clone https://github.com/tapparelj/gr-lora_sdr.git
cd gr-lora_sdr
mkdir -p build && cd build
cmake ..
make -j$(nproc)  # Usa todos los núcleos disponibles en lugar de solo 4 fijo
sudo make install
sudo ldconfig

echo "--- Installation complete! ---"
echo "Rebooting in 5 seconds... Press Ctrl+C to cancel."
sleep 5
sudo reboot