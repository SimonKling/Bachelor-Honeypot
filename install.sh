#!/bin/bash

# Define username and password
USERNAME="honeypot"
PASSWORD="Pueb7oTa8ak876!@"

# Install expect
sudo apt-get update
sudo apt-get install -y expect

# Add the user without a password
sudo adduser --disabled-password --gecos "" $USERNAME

# Add the user to sudo group
sudo usermod -aG sudo $USERNAME

# Set the password for the user
echo "$USERNAME:$PASSWORD" | sudo chpasswd

echo "User $USERNAME created and password set."

# Clone the T-Pot repository as the honeypot user
sudo -u $USERNAME git clone https://github.com/telekom-security/tpotce.git /home/$USERNAME/tpotce

# Copy custom files (if needed)
sudo cp -r galah_tpot /home/$USERNAME/tpotce/docker/
sudo cp docker-compose-custom-bachelor.yml /home/$USERNAME/tpotce/compose

su - $USERNAME 

