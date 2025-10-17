#!/bin/bash

# Maven Drive Copilot - Startup Script
# This script installs dependencies and starts both frontend and backend services

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Clear screen
clear

echo "======================================"
echo "  Maven Drive Copilot Startup Script  "
echo "======================================"
echo ""

# Check prerequisites
print_info "Checking prerequisites..."

if ! command_exists node; then
    print_error "Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

if ! command_exists npm; then
    print_error "npm is not installed. Please install npm and try again."
    exit 1
fi

if ! command_exists python3; then
    print_error "Python 3 is not installed. Please install Python 3.9+ and try again."
    exit 1
fi

# Check for Python 3.12 specifically
PYTHON_CMD="python3.12"
if ! command_exists python3.12; then
    print_warning "Python 3.12 not found, trying python3.11..."
    PYTHON_CMD="python3.11"
    if ! command_exists python3.11; then
        print_warning "Python 3.11 not found, using default python3..."
        PYTHON_CMD="python3"
        print_warning "Note: Python 3.13 may have compatibility issues. Python 3.12 is recommended."
    fi
fi

print_info "Using Python: $PYTHON_CMD ($($PYTHON_CMD --version))"
print_success "All prerequisites found!"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Backend Setup
print_info "Setting up backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment with $PYTHON_CMD..."
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created!"
else
    print_info "Virtual environment already exists."
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate || {
    # For Windows Git Bash or different shells
    source venv/Scripts/activate 2>/dev/null || {
        print_error "Could not activate virtual environment"
        exit 1
    }
}

# Install/upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet

# Install Python dependencies
print_info "Installing Python dependencies..."
pip install -r requirements.txt --quiet
print_success "Python dependencies installed!"

# Check if .env exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found!"
    if [ -f ".env.example" ]; then
        print_info "Copying .env.example to .env..."
        cp .env.example .env
        print_warning "Please edit backend/.env with your credentials before the services start!"
        print_warning "You need to add:"
        echo "  - GOOGLE_CLIENT_ID"
        echo "  - GOOGLE_CLIENT_SECRET"
        echo "  - API keys for your chosen vector DB and LLM"
        echo ""
        read -p "Press Enter to continue after you've updated .env, or Ctrl+C to exit..."
    else
        print_error ".env.example not found. Please create .env file manually."
        exit 1
    fi
else
    print_info ".env file found."
fi

cd ..

# Frontend Setup
print_info "Setting up frontend..."
cd frontend

# Install Node dependencies
if [ ! -d "node_modules" ]; then
    print_info "Installing Node.js dependencies (this may take a few minutes)..."
    npm install
    print_success "Node.js dependencies installed!"
else
    print_info "Node modules already installed. Running npm install to check for updates..."
    npm install
    print_success "Dependencies updated!"
fi

cd ..

print_success "All dependencies installed!"
echo ""

# Check if ports are available
print_info "Checking if ports 3000 and 8000 are available..."

PORT_8000_IN_USE=false
PORT_3000_IN_USE=false

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    PORT_8000_IN_USE=true
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    PORT_3000_IN_USE=true
fi

if [ "$PORT_8000_IN_USE" = true ] || [ "$PORT_3000_IN_USE" = true ]; then
    print_warning "One or more ports are already in use:"
    if [ "$PORT_8000_IN_USE" = true ]; then
        echo "  - Port 8000 (Backend)"
        lsof -i :8000 | head -5
    fi
    if [ "$PORT_3000_IN_USE" = true ]; then
        echo "  - Port 3000 (Frontend)"
        lsof -i :3000 | head -5
    fi
    echo ""
    print_warning "Would you like to stop existing processes and continue? (y/n)"
    read -p "> " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Stopping existing processes..."
        ./stop.sh
        sleep 2
        print_success "Existing processes stopped!"
    else
        print_error "Cannot start services while ports are in use."
        print_info "Run ./stop.sh manually to stop existing services."
        exit 1
    fi
fi

print_success "Ports are available!"
echo ""

# Create log directory
mkdir -p logs

print_info "Starting services..."
echo ""

# Start backend in background
print_info "Starting backend on http://localhost:8000..."
cd backend
source venv/bin/activate || source venv/Scripts/activate 2>/dev/null
python -m src.main > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd ..

# Wait a bit for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    print_error "Backend failed to start. Check logs/backend.log for details."
    cat logs/backend.log
    exit 1
fi

print_success "Backend started! (PID: $BACKEND_PID)"

# Start frontend in background
print_info "Starting frontend on http://localhost:3000..."
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..

# Wait a bit for frontend to start
sleep 3

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    print_error "Frontend failed to start. Check logs/frontend.log for details."
    cat logs/frontend.log
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

print_success "Frontend started! (PID: $FRONTEND_PID)"

echo ""
echo "======================================"
print_success "All services are running!"
echo "======================================"
echo ""
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Logs:"
echo "  Backend:  logs/backend.log"
echo "  Frontend: logs/frontend.log"
echo ""
print_info "To view logs in real-time:"
echo "  Backend:  tail -f logs/backend.log"
echo "  Frontend: tail -f logs/frontend.log"
echo ""
print_warning "To stop all services, run: ./stop.sh"
print_warning "Or press Ctrl+C (note: this may not stop background processes)"
echo ""

# Save PIDs for stop script
echo "BACKEND_PID=$BACKEND_PID" > .pids
echo "FRONTEND_PID=$FRONTEND_PID" >> .pids

# Keep script running and tail logs
print_info "Showing combined logs (Ctrl+C to exit)..."
echo ""
tail -f logs/backend.log logs/frontend.log
