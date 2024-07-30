#!/bin/bash

# Define username and password
USERNAME="honeypot"
PASSWORD="Pueb7oTa8ak876!@"

# Add the user without a password
sudo adduser --disabled-password --gecos "" $USERNAME

sudo usermod -aG sudo $USERNAME
# Set the password
echo "$USERNAME:$PASSWORD" | sudo chpasswd

echo "User $USERNAME created and password set."

# Install expect
sudo apt-get install -y expect

# Clone the T-Pot repository as the honeypot user
sudo -u $USERNAME git clone https://github.com/telekom-security/tpotce.git /home/$USERNAME/tpotce

# Copy custom file (if needed)
sudo cp galah_tpot /home/$USERNAME/tpotce/docker/

sudo cp docker-compose-custom-bachelor.yml /home/$USERNAME/tpotce/compose

su - $USERNAME -c "cd /home/$USERNAME/
