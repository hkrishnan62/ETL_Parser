#!/bin/bash
# ETL Parser Desktop - Linux/macOS Installation Script
# This script installs dependencies and runs the desktop application

set -e  # Exit on error

echo "================================================================================"
echo "                  ETL Parser - Desktop Application Setup"
echo "================================================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo
    echo "Please install Python 3.8 or higher:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    exit 1
fi

echo "Step 1/4: Checking Python installation..."
python3 --version
echo

# Install system dependencies for Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Step 2/4: Installing system dependencies (Linux)..."
    
    # Check if running on Ubuntu/Debian
    if command -v apt-get &> /dev/null; then
        echo "Detected Debian/Ubuntu. Installing GTK dependencies..."
        sudo apt-get update
        sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0
    fi
    
    # Check if running on Fedora/RHEL
    if command -v dnf &> /dev/null; then
        echo "Detected Fedora/RHEL. Installing GTK dependencies..."
        sudo dnf install -y python3-gobject gtk3 webkit2gtk3
    fi
    echo
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Step 2/4: macOS detected - PyObjC will be installed with pip"
    echo
else
    echo "Step 2/4: Unknown OS - skipping system dependencies"
    echo
fi

echo "Step 3/4: Installing Python requirements..."
python3 -m pip install --upgrade pip
python3 -m pip install -r desktop_requirements.txt
echo

echo "Step 4/4: Starting ETL Parser Desktop Application..."
echo
echo "The desktop application window will open in a few seconds..."
echo

# Start the desktop app
python3 desktop_app.py

echo
echo "Application closed."
