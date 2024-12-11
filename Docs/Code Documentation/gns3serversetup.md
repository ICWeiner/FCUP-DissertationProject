create container

# Dependencies

apt install python3 python3-pip pipx qemu-system-x86 libvirt-clients libvirt-daemon-system software-properties-common ca-certificates gnupg2 git cmake libelf-dev libpcap-dev rsync

pipx install gns3-server

pipx ensurepath

pipx completions

eval "$(register-python-argcomplete pipx)"

# VPCS SETUP

git clone https://github.com/GNS3/vpcs.git

cd GNS3/images/vpcs/src

./mk.sh

mv vpcs /usr/bin/

cd

rm -r vpcs/

# UBRIDGE SETUP

git clone https://github.com/GNS3/ubridge.git

cd ubridge/

make

make install

cd

rm -r ubridge/

# DYNAMIPS SETUP

git clone https://github.com/GNS3/dynamips.git

cd dynamips

mkdir build

cd build

cmake ..