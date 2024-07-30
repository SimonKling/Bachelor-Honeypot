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

# Change to the tpotce directory
cd /home/$USERNAME/tpotce

# Run the install script using expect
sudo -u $USERNAME expect <<EOF
  spawn bash install.sh
  expect "Install? (y/n)" { send "y\r" }
  expect "password for $USERNAME:" {send "$PASSWORD\r"}
  expect "Install Type? (h/s/m)" {send "h\r"}
  expect "Enter your web user name:" {send "honeypot\r"}
  expect "Enter password for your web user:" {send "$PASSWORD\r"}
  expect "Repeat password you your web user:" {send "$PASSWORD\r"}
  expect "Is this correct?" {send "y\r"}
  expect eof
EOF

# Copy docker-compose.yml

echo "T-Pot installation completed."
