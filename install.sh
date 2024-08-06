# Description: This script installs T-Pot on a fresh Ubuntu 24.04 installation.

# Define username and password
USERNAME="admin"
PASSWORD="Pueb7oTa8ak876!@"

# Check for the -nouser option
if [ "$1" != "-nouser" ]; then
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
else
    echo "Skipping user creation as -nouser flag is set."
fi

# Clone the T-Pot repository
if [ "$1" != "-nouser" ]; then
    sudo -u $USERNAME git clone https://github.com/telekom-security/tpotce.git /home/$USERNAME/tpotce
else
    git clone https://github.com/telekom-security/tpotce.git ~/tpotce
fi

# Copy custom files 
if [ "$1" != "-nouser" ]; then
    sudo cp -r galah_tpot /home/$USERNAME/tpotce/docker/
    sudo cp docker-compose-custom-bachelor.yml /home/$USERNAME/tpotce/compose
else
    cp -r galah_tpot ~/tpotce/docker/
    cp docker-compose-custom-bachelor.yml ~/tpotce/compose
fi

if [ "$1" != "-nouser" ]; then
    su - $USERNAME
else
    echo "Finished without user creation."
fi
