Install ubuntu server non minimized

sudo apt update -y

sudo apt upgrade -y

cd /tmp

curl https://raw.githubusercontent.com/GNS3/gns3-server/master/scripts/remote-install.sh > 

gns3-remote-install.sh

# might have to remove code that verifies if ubuntu is LTS version... 

sudo bash gns3-remote-install.sh --with-iou --with-i386-repository 

# add templates as needed
# P.S. gns3 web is still in beta and, in particular has a few bugs related to adding templates, consider trying gns3 gui to add templates