---
layout: default
title: Quick Start
nav_order: 2
---


# Prerequisites

## Hardware requirement
Flora expects the system to have at least 50GB of free disk space.
To use Flora for over-the-air communication with phone devices, you need an RF front-end connected with the server via USB 3. Flora has been tested with the following hardware:
- USRP B200, B210
- USRP X300



## Software requirement
Flora currently supports OS Ubuntu 16 and 18. You can opt to install a low-latency kernel for performance, see [this guide](https://gitlab.eurecom.fr/oai/openairinterface5g/-/wikis/OpenAirKernelMainSetup).


# Testbed setup
Flora provides a quick one-step installation script. To run it, simply do

![testbed](../figures/testbed.png)


```bash
    [flora]$ cd testbed-setup/scripts/OAI
    [flora/testbed-setup/scripts/OAI]$ chmod +x install.sh
    [flora/testbed-setup/scripts/OAI]$ ./install.sh
```


This script will install all the necessary software and Flora. To start the system, connect USRP to the computer via USB3.0, and run
```bash
    [flora]$ cd testbed-setup/scripts/OAI
    [flora/testbed-setup/scripts/OAI]$ chmod +x install.sh
    [flora/testbed-setup/scripts/OAI]$ ./run.sh
```

Flora also provides a user with software that can write SIM profile into a Javacard. you can purchase a blank Javacard and request the software download from [here](http://metro.cs.ucla.edu/codeshare.html). Please fill in the form and we will provide you with the link as soon as possible. Follow the instructions provided along with the software and load the correct credential into the Javacard.  

Insert the programmed Javacard into any commercial off-the-shelf device. Set the APN to `oai.ipv4`. Enable roaming on your phone device if applicable. If the device is not automatically connected to the network after a while, try manually searching the mobile network.


# Base station analysis
Flora has been integrated with a built-in analysis feature. After `run.sh`, the log will be saved as `log.mi2log.enb`. 

You can create a Python script to process the log. An example can be found [here](). First create an `OfflineReplayer` and set the input path
```python
src = OfflineReplayer()
src.set_input_path(sys.argv[1])
```
The replayer then feeds the log into an analyzer 
```python
analyzer = RBAnalyzer()
analyzer.set_source(src)
src.run() 
```

An analyzer decodes the input log and enables analysis. An example can be found [here](). To run it, call
```bash
 [flora/enb-analyssis] $ python3 offline-rb.py examples/example_log.txt
```

In the file `offline-rb.py`, a callback function is registered in ``__init__``, which will be called when a message is detected from the log
```python
def __init__(self):
        Analyzer.__init__(self)
        self.add_source_callback(self.__msg_callback)
```
You can then read the messages and process them. Different messages can be used to analyze different LTE protocols
```python
def __msg_callback(self, msg):
  if msg.type_id == "LTE_PHY_PDSCH_Stat_Indication":
    records = msg.data['Records']
``` 

Currently, put you analyzer and replayer as the following structure
```
|- your_analyzer.py
|- your_offline_replayer.py
|- mobile_insight_enb
  |- analyzer
  |- monitor
```



# Enable mobility and carrier aggregation support
We provide advanced feature for 4G/5G mobility support, including
**Carrier aggregation** and **Intra-eNodeB handover**.
Both features are supported for commodity phones.

## Hardware requirement
These premium features are only supported if the base station can run multiple cells. We have deployed and tested on USRP X300 as the base station's radio module.


## Enabling features
You could then follow the installation steps in [this link](https://github.com/Project-Flora/Flora/blob/master/testbed-setup/scripts/srsRAN/README.md) to install one or both of the advanced features.



# # Edge applications
We provide example applications for edge computing.
After the device established the connection with the testbed, you can install an edge application either in the server that is running Flora, or another server that is connected in LAN.
Please request the VR edge computing software from [here](http://metro.cs.ucla.edu/codeshare.html).

