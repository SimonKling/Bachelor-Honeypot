spawn ./install.sh
expect "### Install ? (y/n)"
send "y\r"
expect "### Enter your web user name:"
send "honeypot\r"
expect "### Is this correct? (y/n)"
send "y\r"
expect "### Enter password for your web user:"
send "Pueb7oTa8ak876!@\r"
exspect "### Repeat password you your web user:"
send "Pueb7oTa8ak876!@\r"
expect eof