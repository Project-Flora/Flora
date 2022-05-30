Hardware
--------
Our release supports intra-eNodeB handover with software-defined base station and COTS UE. We need the following hardwares to run handover:
* Server on Ubuntu 18.04
* USRP X300 as the base station's radio module
* COTS UE

[comment]: <> (Intra-eNB handover has been tested successfully on USRP X300 which has two daughter boards to support two cells within one base station.)

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

Open another terminal and run eNB. One has to specify configuration files to enable intra-eNB handover:
```
sudo srsenb --enb_files.rr_config ./rr-ho.conf
```

One can enable network searching on the UE, and select the customized operator to force connection.
Once the connection is successfully set up, you will see output similar as follows: 
```
User 0x46 connected
```

If handover happens and the device successfully switches to another cell, you will see the eNB sends out the command the client gets connected again:
```
[ho-debug] Send out handover command.
(process of acquiring new connectiong)
User 0x46 connected
```

Demo
----
The [demo video](https://youtu.be/-R5dfjVLfeQ) shows the experience of running intra-eNB handover on Google Pixel.
