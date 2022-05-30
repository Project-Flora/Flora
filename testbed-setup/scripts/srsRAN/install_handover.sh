#! /bin/bash

set -e

echo "Installing Prerequisites"
sudo apt-get -y update
sudo apt-get -y install git

sudo apt-get install build-essential cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libsctp-dev

echo "Installing UHD host"
sudo apt-get install libuhd-dev libuhd3.15.0 uhd-host

echo "Installing srsLTE from GitHub repo"
git clone https://github.com/srsran/srsRAN.git
cd srsRAN
git fetch origin refs/tags/release_20_04_2
git checkout tags/release_20_04_2 -b flora_handover
git apply ../handover.patch

mkdir build
cd build
cmake ../
make
sudo make install
srslte_install_configs.sh user
