#!/bin/bash
# /\
# |
# bash shabang (for making it executable)

# update the packages
sudo apt-get update
sudo apt-get upgrade

# apt installs
sudo apt install vim htop cmatrix zsh git net-tools zip unzip ufw python3 python3-pip tmux gnupg -y

# install my zshrc ( as its my install scrip)
wget https://github.com/voidapex11/code-snippets/blob/main/linux/.zshrc

# set shell to zsh
chsh -s $(which zsh)

# install fastfetch
REPO="fastfetch-cli/fastfetch"
LATEST_RELEASE=$(curl -s "https://api.github.com/repos/$REPO/releases/latest")
VERSION=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep -oP '"tag_name":\s*"\K[^"]+')

wget https://github.com/$REPO/releases/download/$VERSION/fastfetch-linux-aarch64.deb
sudo dpkg -i fastfetch-linux-aarch64.deb
rm fastfetch-linux-aarch64.deb

# install gping
echo 'deb [signed-by=/usr/share/keyrings/azlux.gpg] https://packages.azlux.fr/debian/ bookworm main' | sudo tee /etc/apt/sources.list.d/azlux.list
sudo apt install gpg
curl -s https://azlux.fr/repo.gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/azlux.gpg > /dev/null
sudo apt update
sudo apt install gping

# install node js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

nvm install node

# install tldr
npm install -g tldr

# curses for pinentry in gpg
echo you want curses pinentry not the default
sleep 2
sudo update-alternatives --config pinentry
