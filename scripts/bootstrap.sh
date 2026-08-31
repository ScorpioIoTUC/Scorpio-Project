#!/bin/bash

set -euo pipefail

MODE="${1:---all}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
    echo "Usage: $0 [--all|--host-only|--docker-only|--help]"
}

ensure_docker() {
    if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
        echo "[docker] Docker and Docker Compose plugin already installed."
        return
    fi

    if ! command -v apt-get >/dev/null 2>&1; then
        echo "[docker] Unsupported package manager: apt-get was not found."
        exit 1
    fi

    . /etc/os-release
    architecture="$(dpkg --print-architecture 2>/dev/null || echo unknown)"
    echo "[docker] Installing Docker for ${ID:-unknown} ${VERSION_CODENAME:-unknown} (${architecture})..."

    sudo apt-get update -y

    # Debian Trixie provides the Compose v2 plugin through docker-compose,
    # while the official Docker repository uses docker-compose-plugin.
    if apt-cache show docker-compose-plugin 2>/dev/null | grep -q '^Package:'; then
        sudo apt-get install -y docker.io docker-compose-plugin
    elif apt-cache show docker-compose 2>/dev/null | grep -q '^Package:'; then
        sudo apt-get install -y docker.io docker-compose
    else
        echo "[docker] No compatible Docker Compose package was found."
        echo "[docker] Configure Docker's official repository or install Docker manually."
        exit 1
    fi

    if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
        echo "[docker] Docker Compose installation could not be verified."
        exit 1
    fi

    echo "[docker] $(docker --version)"
    echo "[docker] $(docker compose version)"
}

run_host() {
    echo "[host] Running Raspberry Pi host dependency installation..."
    cd "$PROJECT_ROOT"
    bash ./dependencies.sh --no-reboot
    echo "[host] Host setup complete. A reboot is recommended before Docker setup."
}

run_docker() {
    echo "[docker] Preparing Docker environment..."
    ensure_docker

    # Add current user to docker group; no-op if already present.
    sudo usermod -aG docker "$USER" || true

    echo "[docker] Building and starting infrastructure..."
    cd "$PROJECT_ROOT"
    # Levanta infraestructura sin depender de un target "up" en Makefile.
    if docker info >/dev/null 2>&1; then
        docker compose -f deploy/docker-compose.yml up -d --build
        docker compose -f deploy/docker-compose.yml ps
    else
        echo "[docker] Docker permission denied; retrying with sudo..."
        sudo docker compose -f deploy/docker-compose.yml up -d --build
        sudo docker compose -f deploy/docker-compose.yml ps
    fi

    echo "[docker] Infrastructure is up."
    echo "[docker] If permission issues persist, re-login and rerun: $0 --docker-only"
}

case "$MODE" in
    --all)
        run_host
        echo ""
        echo "Reboot now, then run:"
        echo "  ./scripts/bootstrap.sh --docker-only"
        ;;
    --host-only)
        run_host
        ;;
    --docker-only)
        run_docker
        ;;
    --help|-h)
        usage
        ;;
    *)
        echo "Unknown argument: $MODE"
        usage
        exit 1
        ;;
esac
