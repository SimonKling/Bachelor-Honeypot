cd tpotce/
### Run the install script
  spawn bash install.sh
  expect "Install? (y/n)" { send "y\r" }
  expect "Install Type? (h/s/m)" {send "h\r"}
  expect "Enter your web user name:" {send "honeypot\r"}
  expect "Is this correct?" {send "y\r"}
  expect "Enter password for your web user:" {send "$PASSWORD\r"}
  expect "Repeat password you your web user:" {send "$PASSWORD\r"}
  expect eof