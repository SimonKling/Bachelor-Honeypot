#!/bin/bash

# Define username and password
USERNAME="honeypot"
PASSWORD="Pueb7oTa8ak876!@"
WEB_USERNAME="admin"
WEB_PASSWORD="AdminSecurePass123!"

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
sudo cp galah_tpot /home/$USERNAME/tpotce/docker/
sudo cp docker-compose-custom-bachelor.yml /home/$USERNAME/tpotce/compose

# Create expect script
cat <<EOF > /home/$USERNAME/tpotce/install.expect
#!/usr/bin/expect -f

# Start the install script
spawn ./install.sh

# Expect the install prompt and respond with "y"
expect "### Install ? (y/n)"
send "y\r"

# Expect the sudo password prompt and provide the password
expect "password for $USERNAME:"
send "$PASSWORD\r"

# Expect the install type prompt and respond with "h" (or "s"/"m" as needed)
expect "### Install Type? (h/s/m)"
send "h\r"

# Expect the web username prompt and provide the username
expect "### Enter your web user name:"
send "$WEB_USERNAME\r"

# Expect the confirmation prompt and respond with "y"
expect "### Is this correct? (y/n)"
send "y\r"

# Expect the web user password prompt and provide the password
expect "### Enter password for your web user:"
send "$WEB_PASSWORD\r"

# Expect the repeat password prompt and provide the password again
expect "### Repeat password you your web user:"
send "$WEB_PASSWORD\r"

# Wait for the script to finish
expect eof
EOF

# Make the expect script executable
sudo chmod +x /home/$USERNAME/tpotce/install.expect

# Run the expect script as the honeypot user
su - $USERNAME -c "cd /home/$USERNAME/tpotce && ./install.expect"

echo "Installation script executed."
