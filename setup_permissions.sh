#!/bin/bash
# Script to setup permissions for Thockify on Linux/Wayland

if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root (sudo ./setup_permissions.sh)"
  exit
fi

echo "Adding user '$SUDO_USER' to 'input' group..."

# Create group if it doesn't exist (it usually does)
groupadd -f input

# Add user
usermod -aG input $SUDO_USER

echo "Done!"
echo "IMPORTANT: You must LOG OUT and LOG BACK IN for this to take effect."
echo "after that, run 'python main.py' normally."
