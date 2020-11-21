echo "Start System"
cd $OPENAIR_DIR/cmake_targets/lte_build_oai/build
sudo -E ./lte-softmodem -O $OPENAIR_DIR/targets/PROJECTS/GENERIC-LTE-EPC/CONF/test.conf -d > log.mi2log.enb