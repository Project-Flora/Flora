#! /bin/bash

set -e

echo "Installing Prerequisites"
sudo apt-get -y install git
git clone https://gitlab.eurecom.fr/oai/openairinterface5g.git
git clone https://github.com/magma/magma.git
sudo apt-get -y update
sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
    virtualbox python3-pip \
    ansible
sudo apt-get -y update
curl -O https://releases.hashicorp.com/vagrant/2.2.6/vagrant_2.2.6_x86_64.deb
sudo apt-get -y install ./vagrant_2.2.6_x86_64.deb
vagrant --version
vagrant plugin install vagrant-vbguest
pip3 install ansible fabric3 requests PyYAML jsonpickle
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get -y update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose


echo "Installing eNB from OAI"
cd openairinterface5g
git checkout 7af8412
patch -p1 < ../MI-eNB_patch.patch
source oaienv
cd cmake_targets
./build_oai -I --eNB -x --install-system-files -w USRP
cp ../../test.conf ../targets/PROJECTS/GENERIC-LTE-EPC/CONF/
cd ../../

echo "Installing EPC from magma"
cd magma
git checkout v1.0.0
cd lte/gateway
sudo vagrant up
cd ../..
cd orc8r/cloud/docker
sudo PWD=$(pwd) ./build.py
sudo PWD=$(pwd) docker-compose up -d

cd ../../../
cd lte/gateway
sudo vagrant ssh -c "cd magma/lte/gateway && make run"
sudo vagrant ssh -c "echo 1 > tmp.txt && sudo cp tmp.txt /proc/sys/net/ipv4/conf/eth0/proxy_arp && rm tmp.txt"
sudo ~/.local/bin/fab -f dev_tools.py register_vm

