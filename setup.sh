#!/bin/bash

# Define Python version to install (you can update this as needed)
python_version="3.9.7"

# Function to show a loading animation
function show_loading() {
    local pid=$!
    local spin='-\|/'
    local i=0
    while kill -0 $pid 2>/dev/null; do
        i=$(( (i+1) % 4 ))
        printf "\r[%c] Installing..." "${spin:$i:1}"
        sleep 0.1
    done
    printf "\r[✓] Installed.     \n"
}

# Install Python
echo "Installing Python $python_version"
python_installer="python-installer.exe"

# Download Python installer using curl
curl -o "$python_installer" "https://www.python.org/ftp/python/$python_version/python-$python_version-amd64.exe" && show_loading

# Run the Python installer silently
"$python_installer" /quiet

# Install pip (ensurepip)
echo "Installing pip"
python -m ensurepip --default-pip & show_loading

# Clone a GitHub project
echo "Cloning a GitHub project"
git clone https://github.com/Konsa-College/UPTU-IPU-Choice-Filling-Automation-Setup.git & show_loading

# Navigate to the Git repository directory
cd UPTU-IPU-Choice-Filling-Automation-Setup

# Install Libraries from requirements.txt
echo "Installing libraries from requirements.txt"
pip install -r requirements.txt & show_loading

# Open the choice_filling.csv file
echo "Opening choice_filling.csv"
# Replace the following line with the appropriate command to open CSV file with the default program on your system
# Example: On Windows, you can use start
start choice_filling.csv

# Run main.py (once)
# echo "Running main.py"
# python main.py

echo "Script completed."
