Hardware
--------
Our release supports carrier aggregation with software-defined base station and COTS UE. We need the following hardwares to run CA:
* Server on Ubuntu 18.04
* USRP X300 as the base station's radio module
* COTS UE

[comment]: <> (The CA function has been tested successfully on USRP X300 which has two daughter boards to support two-carrier aggregation.)

Installation
------------

On Ubuntu 18.04, the user can run the all-in-one script to install and build the project:
```
sudo ./install.sh
```

Configuration
-------------
One has to edit the configuration files properly to connect eNB to EPC, authenticate COTS UE, and access the Internet on UE.
* In file ``~/.config/srslte/user_db.csv``, add the SIM card credentials so that EPC can authenticate the UE.
* In both ``~/.config/srslte/enb.conf`` and ``~/.config/srslte/epc.conf configure``, configure fields ``mcc,mnc`` and make sure they are consistent in two files.
* In file ``~/.config/srslte/enb.conf``, configure the bandwidth of one cell to 5MHz by using the following line (replacing the original value if any):
```
n_prb = 25
```
* To access the Internet, one has to [configure APN](https://docs.srsran.com/en/latest/app_notes/source/cots_ue/source/index.html#adding-an-apn) on both the UE and eNB and [run masquerading script](https://docs.srsran.com/en/latest/app_notes/source/cots_ue/source/index.html#run-masquerading-script).

Execution
---------
srsENB and srsEPC can run on the same machine.

### srsEPC

Open one terminal and run the EPC:
```
sudo srsepc
```

### srsENB

Open another terminal and run eNB. One has to specify configuration files to enable CA:
```
sudo srsenb --enb_files.rr_config ./rr-2ca.conf
```

One can enable network searching on the UE, and select the customized operator to force connection.
The connection is successfully set up and CA gets enables when you see output similar as follows:
```
User 0x46 connected
[ca-debug] Added SCell Activation CE; Finish allocating and initializing buffers, num=2
```

Demo
----
The [demo video](https://youtu.be/36PUAmyAPs0) shows the experience of running CA on Google Pixel.
