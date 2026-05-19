#!/bin/bash
# Install LoRa Decoder as systemd service

set -e

CURRENT_USER=$(whoami)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_NAME="lora-decoder"
SERVICE_FILE="${SERVICE_NAME}@${CURRENT_USER}.service"
DECODER_DIR="${PROJECT_DIR}/decoder/lora-decoder"
SYSTEMD_DIR="/etc/systemd/system"

echo "[*] Installing LoRa Decoder as systemd service..."
echo "[*] Project directory: $PROJECT_DIR"
echo "[*] User: $CURRENT_USER"

# Verify lora_decoder.py exists
if [ ! -f "${DECODER_DIR}/lora_decoder.py" ]; then
    echo "[ERROR] lora_decoder.py not found at ${DECODER_DIR}/lora_decoder.py"
    exit 1
fi

# Create a dedicated virtualenv for the decoder (run as current user)
DECODER_VENV="${DECODER_DIR}/venv"
if [ ! -d "${DECODER_VENV}" ]; then
    echo "[*] Creating python virtualenv at ${DECODER_VENV}"
    python3 -m venv "${DECODER_VENV}"
    "${DECODER_VENV}/bin/pip" install --upgrade pip
    if [ -f "${PROJECT_DIR}/requirements.txt" ]; then
        echo "[*] Installing Python requirements into decoder venv"
        "${DECODER_VENV}/bin/pip" install -r "${PROJECT_DIR}/requirements.txt"
    else
        echo "[WARN] requirements.txt not found at ${PROJECT_DIR}; installing paho-mqtt into venv"
        "${DECODER_VENV}/bin/pip" install paho-mqtt
    fi
else
    echo "[*] Using existing virtualenv at ${DECODER_VENV}"
fi

# Check if we have sudo
if ! sudo -n true 2>/dev/null; then
    echo "[!] This script requires sudo. You will be prompted for your password."
fi

# Copy service file
echo "[*] Installing service file to $SYSTEMD_DIR/$SERVICE_FILE"
sudo cp "${DECODER_DIR}/lora-decoder.service" "$SYSTEMD_DIR/${SERVICE_FILE}"

# Enable service
echo "[*] Enabling service..."
sudo systemctl daemon-reload
sudo systemctl enable "${SERVICE_FILE}"

# Check if service is already running
if sudo systemctl is-active --quiet "${SERVICE_FILE}"; then
    echo "[*] Service is already running. Restarting..."
    sudo systemctl restart "${SERVICE_FILE}"
else
    echo "[*] Starting service..."
    sudo systemctl start "${SERVICE_FILE}"
fi

echo "[OK] Service installed and started!"
echo ""
echo "Useful commands:"
echo "  Status:  sudo systemctl status lora-decoder@${CURRENT_USER}.service"
echo "  Logs:    sudo journalctl -u lora-decoder@${CURRENT_USER}.service -f"
echo "  Stop:    sudo systemctl stop lora-decoder@${CURRENT_USER}.service"
echo "  Start:   sudo systemctl start lora-decoder@${CURRENT_USER}.service"
