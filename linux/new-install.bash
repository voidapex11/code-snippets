#!/bin/bash
# /\
# |
# bash shabang (for making it executable)

set -x

ARCH="$(uname --machine)"

# update the packages
sudo apt update
sudo apt upgrade

# apt installs
sudo apt install nala -y
sudo nala install zsh-autosuggestions command-not-found btop vim htop cmatrix zsh git net-tools zip unzip ufw python3 python3-pip tmux gnupg ncdu bat rlwrap -y

# install my zshrc ( as its my install scrip)
wget https://raw.githubusercontent.com/voidapex11/code-snippets/refs/heads/main/linux/.zshrc
wget https://raw.githubusercontent.com/voidapex11/code-snippets/refs/heads/main/linux/.p10k.zsh
wget https://raw.githubusercontent.com/voidapex11/code-snippets/refs/heads/main/linux/.tmux.conf

# set shell to zsh
chsh -s $(which zsh)

# install fastfetch
REPO="fastfetch-cli/fastfetch"
LATEST_RELEASE=$(curl -s "https://api.github.com/repos/$REPO/releases/latest")
VERSION=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep -oP '"tag_name":\s*"\K[^"]+')

wget https://github.com/$REPO/releases/download/$VERSION/fastfetch-linux-$ARCH.deb
sudo dpkg -i fastfetch-linux-$ARCH.deb
rm fastfetch-linux-$ARCH.deb

# install cheat.sh
curl -s https://cht.sh/:cht.sh | sudo tee /usr/local/bin/cheat && sudo chmod +x /usr/local/bin/cheat

# install gping
echo 'deb [signed-by=/usr/share/keyrings/azlux.gpg] https://packages.azlux.fr/debian/ bookworm main' | sudo tee /etc/apt/sources.list.d/azlux.list
sudo nala install gpg -y
curl -s https://azlux.fr/repo.gpg.key | gpg --dearmor | sudo tee /usr/share/keyrings/azlux.gpg >/dev/null
sudo nala update
sudo nala install gping -y

# install node js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

nvm install node

# install tldr
npm install -g tldr

# install rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

. "$HOME/.cargo/env" # configure path

# install dust and dysk
#cargo install cargo-binstall
REPO="cargo-bins/cargo-binstall"
LATEST_RELEASE=$(curl -s "https://api.github.com/repos/$REPO/releases/latest")
VERSION=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep -oP '"tag_name":\s*"\K[^"]+')

wget https://github.com/$REPO/releases/download/$VERSION/cargo-binstall-$ARCH-unknown-linux-gnu.tgz
tar -xvzf cargo-binstall-$ARCH-unknown-linux-gnu.tgz
./cargo-binstall cargo-binstall
rm cargo-binstall-$ARCH-unknown-linux-gnu.tgz cargo-binstall

cargo binstall du-dust
cargo binstall --locked dysk
cargo binstall eza

# docker
sudo nala install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" |
  sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
sudo nala update

sudo nala install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

sudo docker run hello-world

# neovim

docker run -d --restart unless-stopped --name nvchad \
  -w "$HOME" \
  -v "$HOME:$HOME" \
  alpine:latest sh -c "\
    apk add git nodejs neovim ripgrep build-base wget --update && \
    git clone https://github.com/NvChad/starter ~/.config/nvim ; \
    tail -f /dev/null"

# curses for pinentry in gpg
echo you want curses pinentry not the default
sleep 2
sudo update-alternatives --config pinentry

git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
