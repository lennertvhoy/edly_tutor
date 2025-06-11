#!/bin/bash

echo "Starting Tutor installation and troubleshooting automation..."

# 1. Install python3-pip if not found
if ! command -v pip &> /dev/null
then
    echo "pip not found, installing python3-pip..."
    sudo apt update && sudo apt install -y python3-pip
fi

# 2. Install python3.12-venv if not found
if ! dpkg -s python3.12-venv &> /dev/null
then
    echo "python3.12-venv not found, installing..."
    sudo apt install -y python3.12-venv
fi

# 3. Create and activate virtual environment
echo "Creating and activating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 4. Install tutor[full] in the virtual environment
echo "Installing tutor[full]..."
pip install "tutor[full]"

# 5. Add user to docker group
echo "Adding current user to docker group (requires password)..."
sudo usermod -aG docker ${USER}

# 6. Modify /etc/wsl.conf
echo "Configuring /etc/wsl.conf to disable automatic resolv.conf generation..."
echo -e "[user]\ndefault = ${USER}\n\n[network]\ngenerateResolvConf = false" | sudo tee /etc/wsl.conf > /dev/null

# 7. Modify /etc/resolv.conf
echo "Configuring /etc/resolv.conf with public DNS servers..."
echo -e "nameserver 8.8.8.8\nnameserver 8.8.4.4" | sudo tee /etc/resolv.conf > /dev/null

echo "Automated steps complete. You MUST fully shut down WSL and restart it."
echo "After restarting WSL, open your Ubuntu terminal, go to your project directory,"
echo "and then run the following commands manually:"
echo "source venv/bin/activate"
echo "tutor local launch"
echo "You will be prompted for configuration in 'tutor local launch'." 