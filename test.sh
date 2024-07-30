#!/bin/bash

# Define username and password
USERNAME="honeypot"
PASSWORD="Pueb7oTa8ak876!@"

# Install expect
sudo apt-get update
sudo apt-get install -y expect

# Add the user without a password
sudo adduser --disabled-password --gecos "" $USERNAME

# Add the user to the sudo group
sudo usermod -aG sudo $USERNAME

# Set the password
echo "$USERNAME:$PASSWORD" | sudo chpasswd

echo "User $USERNAME created and password set."

# Clone the T-Pot repository as the honeypot user
sudo -u $USERNAME git clone https://github.com/telekom-security/tpotce.git /home/$USERNAME/tpotce

# Copy custom file (if needed)
sudo cp galah_tpot /home/$USERNAME/tpotce/docker/
sudo cp docker-compose-custom-bachelor.yml /home/$USERNAME/tpotce/compose

# Create the expect script to automate the T-Pot installation
cat <<EOF > /home/$USERNAME/tpotce/install.expect
#!/usr/bin/expect -f

set timeout -1

spawn ./install.sh

expect "### Install ? (y/n)"
send "y\r"
expect "### Enter your web user name:"
send "$USERNAME\r"
expect "### Is this correct? (y/n)"
send "y\r"
expect "### Enter password for your web user:"
send "$PASSWORD\r"
expect "### Repeat password for your web user:"
send "$PASSWORD\r"
expect eof
EOF

# Change ownership and permissions of the expect script
sudo chown $USERNAME:$USERNAME /home/$USERNAME/tpotce/install.expect
sudo chmod +x /home/$USERNAME/tpotce/install.expect

# Run the expect script as the honeypot user
sudo -u $USERNAME /home/$USERNAME/tpotce/install.expect

echo "T-Pot installation script executed."