#!/bin/bash

echo "Starting Revolver Panel installation..."

if [ -x "$(command -v apt)" ]; then
    echo "Debian/Ubuntu system detected. Installing dependencies..."
    sudo apt update && sudo apt install python3 python3-gi python3-gi-cairo python3-cairo git -y
elif [ -x "$(command -v dnf)" ]; then
    echo "Fedora system detected. Installing dependencies..."
    sudo dnf install python3 python3-gobject python3-cairo git -y
elif [ -x "$(command -v pacman)" ]; then
    echo "Arch Linux system detected. Installing dependencies..."
    sudo pacman -Syu --needed python python-gobject python-cairo git --noconfirm
fi

mkdir -p ~/.config/revolver-panel
cp main.py ~/.config/revolver-panel/main.py

mkdir -p ~/.config/autostart
cat << 'AUTOLOAD' > ~/.config/autostart/revolver_panel.desktop
[Desktop Entry]
Type=Application
Exec=python3 %h/.config/revolver-panel/main.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Revolver Panel
Comment=Circular application launcher
AUTOLOAD

sudo ln -sf ~/.config/revolver-panel/main.py /usr/local/bin/revolver-panel
sudo chmod +x /usr/local/bin/revolver-panel
chmod +x ~/.config/revolver-panel/main.py

echo "Installation completed successfully."
