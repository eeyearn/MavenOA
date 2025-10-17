#!/bin/bash

# Maven Drive Copilot - Stop Script
# This script stops both frontend and backend services

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "======================================"
echo "   Stopping Maven Drive Copilot       "
echo "======================================"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if PID files exist
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    print_info "Stopping backend (PID: $BACKEND_PID)..."

    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        sleep 1

        # Force kill if still running
        if kill -0 $BACKEND_PID 2>/dev/null; then
            print_info "Force stopping backend..."
            kill -9 $BACKEND_PID 2>/dev/null
        fi

        print_success "Backend stopped!"
    else
        print_info "Backend process not running."
    fi

    rm logs/backend.pid
else
    print_info "No backend PID file found."
fi

if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    print_info "Stopping frontend (PID: $FRONTEND_PID)..."

    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        sleep 1

        # Force kill if still running
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            print_info "Force stopping frontend..."
            kill -9 $FRONTEND_PID 2>/dev/null
        fi

        print_success "Frontend stopped!"
    else
        print_info "Frontend process not running."
    fi

    rm logs/frontend.pid
else
    print_info "No frontend PID file found."
fi

# Also kill any remaining processes on ports 3000 and 8000
print_info "Checking for any remaining processes on ports 3000 and 8000..."

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_info "Found process on port 8000, stopping..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_info "Found process on port 3000, stopping..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null
fi

# Clean up PID file
if [ -f ".pids" ]; then
    rm .pids
fi

echo ""
print_success "All services stopped!"
echo ""
