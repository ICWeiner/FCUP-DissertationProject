create container

apt install pipx qemu-user-static git cmake libelf-dev libpcap0.8-dev

pipx install gns3-server

pipx ensurepath

pipx completions

eval "$(register-python-argcomplete pipx)"

git clone https://github.com/GNS3/dynamips.git

cd dynamips

mkdir build

cd build

cmake ..