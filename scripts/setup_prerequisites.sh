#!/bin/bash
# Setup script for sdd-adk-agents-agy codelab prerequisites.
# Checks for and installs required tools. Skips anything already installed.

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok() { echo -e "  ${GREEN}✓${NC} $1"; }
missing() { echo -e "  ${YELLOW}✗${NC} $1"; }

echo ""
echo "=== Checking prerequisites ==="
echo ""

# --- git ---
if command -v git &>/dev/null; then
    ok "git $(git --version | awk '{print $3}')"
else
    missing "git not found — installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update -qq && sudo apt-get install -y -qq git
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        xcode-select --install 2>/dev/null || true
    fi
    ok "git installed"
fi

# --- curl ---
if command -v curl &>/dev/null; then
    ok "curl $(curl --version | head -1 | awk '{print $2}')"
else
    missing "curl not found — installing..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update -qq && sudo apt-get install -y -qq curl
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install curl
    fi
    ok "curl installed"
fi

# --- gcloud CLI ---
if command -v gcloud &>/dev/null; then
    ok "gcloud $(gcloud version 2>/dev/null | head -1 | awk '{print $4}')"
else
    missing "gcloud CLI not found — installing..."
    curl -sSL https://sdk.cloud.google.com | bash -s -- --disable-prompts
    # Source the path so gcloud is available in the current session
    if [ -f "$HOME/google-cloud-sdk/path.bash.inc" ]; then
        source "$HOME/google-cloud-sdk/path.bash.inc"
    elif [ -f "$HOME/google-cloud-sdk/path.zsh.inc" ]; then
        source "$HOME/google-cloud-sdk/path.zsh.inc"
    fi
    ok "gcloud CLI installed"
fi

# --- uv ---
if command -v uv &>/dev/null; then
    ok "uv $(uv --version 2>/dev/null | awk '{print $2}')"
else
    missing "uv not found — installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Source the env so uv is available in the current session
    source "$HOME/.local/bin/env" 2>/dev/null || export PATH="$HOME/.local/bin:$PATH"
    ok "uv installed"
fi

# --- Python 3.12 (managed by uv) ---
if uv python find 3.12 &>/dev/null; then
    ok "Python 3.12 (uv-managed: $(uv python find 3.12))"
else
    missing "Python 3.12 not found — installing via uv..."
    uv python install 3.12
    ok "Python 3.12 installed via uv"
fi

# --- MCP Toolbox for Databases ---
TOOLBOX_VERSION="0.27.0"
TOOLBOX_DIR="$HOME/.local/bin"
if [ -x "$TOOLBOX_DIR/toolbox" ]; then
    ok "MCP Toolbox ($TOOLBOX_DIR/toolbox)"
else
    missing "MCP Toolbox not found — installing to $TOOLBOX_DIR..."
    mkdir -p "$TOOLBOX_DIR"
    TOOLBOX_OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    TOOLBOX_ARCH=$(uname -m)
    if [ "$TOOLBOX_ARCH" = "x86_64" ]; then TOOLBOX_ARCH="amd64"; elif [ "$TOOLBOX_ARCH" = "aarch64" ] || [ "$TOOLBOX_ARCH" = "arm64" ]; then TOOLBOX_ARCH="arm64"; fi
    curl -so "$TOOLBOX_DIR/toolbox" "https://storage.googleapis.com/genai-toolbox/v${TOOLBOX_VERSION}/${TOOLBOX_OS}/${TOOLBOX_ARCH}/toolbox"
    chmod +x "$TOOLBOX_DIR/toolbox"
    ok "MCP Toolbox installed to $TOOLBOX_DIR/toolbox"
fi

echo ""
echo "=== All prerequisites ready ==="
echo ""
