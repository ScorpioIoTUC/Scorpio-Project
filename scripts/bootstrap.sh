#!/bin/bash

set -euo pipefail

MODE="${1:---all}"
MODULE="${MODULE:-bootstrap}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

log() {
    local level="$1"
    local section="$2"
    local message="$3"
    echo "log:${level}:${MODULE}:${section}:${message}"
}

usage() {
    echo "Usage: $0 [--all|--host-only|--docker-only|--help]"
}

ensure_docker() {
    log info docker_check "Checking Docker installation"
    if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
        log info docker_check "Docker and Docker Compose plugin already installed"
        return
    fi

    if ! command -v apt-get >/dev/null 2>&1; then
        log error docker_check "Unsupported package manager: apt-get was not found"
        exit 1
    fi

    . /etc/os-release
    architecture="$(dpkg --print-architecture 2>/dev/null || echo unknown)"
    log info docker_install "Installing Docker for ${ID:-unknown} ${VERSION_CODENAME:-unknown} (${architecture})"

    sudo apt-get update -y

    # Debian Trixie provides the Compose v2 plugin through docker-compose,
    # while the official Docker repository uses docker-compose-plugin.
    if apt-cache show docker-compose-plugin 2>/dev/null | grep -q '^Package:'; then
        sudo apt-get install -y docker.io docker-compose-plugin
    elif apt-cache show docker-compose 2>/dev/null | grep -q '^Package:'; then
        sudo apt-get install -y docker.io docker-compose
    else
        log error docker_install "No compatible Docker Compose package was found"
        log error docker_install "Configure Docker official repository or install Docker manually"
        exit 1
    fi

    if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
        log error docker_verify "Docker Compose installation could not be verified"
        exit 1
    fi

    log info docker_verify "$(docker --version)"
    log info docker_verify "$(docker compose version)"
}

run_host() {
    log info step:1/2:host_setup "Running Raspberry Pi host dependency installation"
    cd "$PROJECT_ROOT"
    bash ./dependencies.sh --no-reboot
    log info step:1/2:host_setup "Host setup complete. A reboot is recommended before Docker setup"
}

run_docker() {
    log info step:2/2:docker_setup "Preparing Docker environment"
    ensure_docker

    # Add current user to docker group; no-op if already present.
    sudo usermod -aG docker "$USER" || true

    log info step:2/2:docker_setup "Building and starting infrastructure"
    cd "$PROJECT_ROOT"

    if docker info >/dev/null 2>&1; then
        docker_command=(docker)
        log info docker_permission "Docker can run without sudo"
    else
        docker_command=(sudo docker)
        log warning docker_permission "Docker permission denied; retrying with sudo"
    fi

    if ! "${docker_command[@]}" network inspect scorpio-net >/dev/null 2>&1; then
        log info docker_network "Creating external network scorpio-net"
        "${docker_command[@]}" network create scorpio-net >/dev/null
    else 
        log info docker_network "External network scorpio-net already exists"
    fi

    log info docker_compose "Running docker compose up"
    "${docker_command[@]}" compose -f deploy/docker-compose.yml up -d --build
    log info docker_compose "Listing running services"
    "${docker_command[@]}" compose -f deploy/docker-compose.yml ps
     
    log info step:2/2:docker_setup "Infrastructure is up"
    log warning docker_permission "If permission issues persist, re-login and rerun: $0 --docker-only"
}

case "$MODE" in
    --all)
        log info mode "Running full setup"
        run_host
        echo "log:warning:${MODULE}:next_action:Reboot now, then run ./scripts/bootstrap.sh --docker-only"
        ;;
    --host-only)
        log info mode "Running host-only setup"
        run_host
        ;;
    --docker-only)
        log info mode "Running docker-only setup"
        run_docker
        ;;
    --help|-h)
        usage
        ;;
    *)
        log error mode "Unknown argument: $MODE"
        usage
        exit 1
        ;;
esac
