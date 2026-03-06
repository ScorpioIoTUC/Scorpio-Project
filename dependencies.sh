#!/bin/bash

# Abortar si hay errores
set -e

echo "--- 1/6 System update and upgrade ---"
sudo apt update && sudo apt full-upgrade -y

echo "--- 2/6 Esscential dependencies ---"
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

echo "--- 3/6 GNU Radio instalation"
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
volk_profile

echo "--- 6/6 GR-LoRa-SDR instalation"
if [ -d "gr-lora_sdr" ]; then rm -rf gr-lora_sdr; fi
git clone https://github.com/tapparelj/gr-lora_sdr.git
cd gr-lora_sdr
mkdir build && cd build
cmake ..
make -j4
sudo make install
sudo ldconfig
cd ../..

echo "--- Instalation complete! Rebooting... ---"
sudo reboot