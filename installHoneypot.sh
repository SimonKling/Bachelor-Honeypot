#!/bin/bash

# Define username and password
USERNAME="honeypot"
PASSWORD="Pueb7oTa8ak876!@"

# Add the user without a password
sudo adduser --disabled-password --gecos "" $USERNAME

# Set the password
echo "$USERNAME:$PASSWORD" | sudo chpasswd

echo "User $USERNAME created and password set."

su - $USERNAME

sudo apt-get install expect

git clone https://github.com/telekom-security/tpotce.git

cp galah_tpot /tpotce/docker/

cd toptce

expect <<EOF
  spawn bash install.sh
  expect "Install? (y/n)" { send "y\r" }
  expect "Install Type? (h/s/m)" {send "h\r"}
  expect eof
EOF

cd .. 

cp /docker-compose.yml /tpotce/

cd tpotce


