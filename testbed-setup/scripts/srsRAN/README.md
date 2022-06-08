# Release v2.0: Carrier Aggregation and Handover 

In this release, two features are added for 4G/5G mobility support:
- Carrier aggregation
- Intra-eNodeB handover

Both features are supported for commodity phones.

## Hardware

We need the following hardwares to run handover:
- Server on Ubuntu 18.04
- USRP X300 as the base station's radio module
- A commodity phone

## Carrier aggregation

### Installation

Run the all-in-one script to install and build the project:

```bash
  [Flora]$ cd testbed-setup/scripts/srsRAN
  [Flora/testbed-setup/scripts/srsRAN]$ chmod +x install_ca.sh
  [Flora/testbed-setup/scripts/srsRAN]$ ./install_ca.sh
```

### Configuration

Edit the configuration files properly to connect eNB to EPC, authenticate the UE, and access the Internet.
* Edit file ``~/.config/srslte/user_db.csv``: add the SIM card credentials so that EPC can authenticate the UE.
* Edit both ``~/.config/srslte/enb.conf`` and ``~/.config/srslte/epc.conf configure``: configure fields ``mcc,mnc`` and make sure they are consistent in two files.
* Edit ``~/.config/srslte/enb.conf``: configure the bandwidth of one cell to 5MHz by using the following line (replacing the original value if any):
```
  n_prb = 25
```
* To access the Internet, one has to [configure APN](https://docs.srsran.com/en/latest/app_notes/source/cots_ue/source/index.html#adding-an-apn) on both the UE and eNB and [run masquerading script](https://docs.srsran.com/en/latest/app_notes/source/cots_ue/source/index.html#run-masquerading-script).

### Execution

srsENB and srsEPC can run on the same machine.

__srsEPC__: Open one terminal and run the EPC:
```bash
  [Flora/testbed-setup/scripts/srsRAN]$ sudo srsepc
```

__srsENB__: Open another terminal and run eNB. One has to specify configuration files to enable CA:
```bash
  [Flora/testbed-setup/scripts/srsRAN]$ sudo srsenb --enb_files.rr_config ./rr-2ca.conf
```

Users can enable network searching on the UE, and select the customized operator to force connection.
The connection is successfully set up and CA gets enables when you see output similar as follows:
```bash
  User 0x46 connected
  [ca-debug] Added SCell Activation CE; Finish allocating and initializing buffers, num=2
```

### Demo

The [demo video](https://youtu.be/36PUAmyAPs0) shows the experience of running CA on Google Pixel.


## Handover

### Installation

On Ubuntu 18.04, run the all-in-one script to install and build the project:

```bash
  [Flora]$ cd testbed-setup/scripts/srsRAN
  [Flora/testbed-setup/scripts/srsRAN]$ chmod +x install_handover.sh
  [Flora/testbed-setup/scripts/srsRAN]$ ./install_handover.sh
```

### Configuration

Apply the same configuration as carrier aggregation.

Due to hardware limitation, handover is performed between two physical cells. Flora can emulate multiple virtual cells identified by different upper-layer configurations.
In release v2.0, Flora supports configurations in terms of various triggering conditions of measurement reports.
To emulate virtual cells, you can add a list of handover settings at the end of ``./rr-ho.conf`` as follows: 

```json
  vcell_list = 
  (
    {
      a3_report_type = "RSRP";
      a3_offset = 6;
      a3_hysteresis = 0;
      a3_time_to_trigger = 480;
    },
    {
      a3_report_type = "RSRP";
      a3_offset = 4;
      a3_hysteresis = 0;
      a3_time_to_trigger = 480;
    }
  );

```

The example includes two virtual cells. Flora supports up to 32 cells.

### Execution

Run srsENB and srsEPC on the same machine.

__srsEPC__: Open one terminal and run the EPC:
```bash
  [Flora/testbed-setup/scripts/srsRAN]$ sudo srsepc
```

__srsENB__: Open another terminal and run eNB with specify configuration file specified to enable intra-eNB handover:
```bash
  [Flora/testbed-setup/scripts/srsRAN]$ sudo srsenb --enb_files.rr_config ./rr-ho.conf
```

Users can enable network searching on the UE, and select the customized operator to force connection.
Once the connection is successfully set up, you will see output similar as follows:
```bash
  User 0x46 connected
```

If handover happens and the device successfully switches to another cell, you will see the eNB sends out the command the client gets connected again:
```bash 
  [ho-debug] Send out handover command.
  (process of acquiring new connectiong)
  User 0x46 connected
```

### Demo

The [demo video](https://youtu.be/-R5dfjVLfeQ) shows the experience of running intra-eNB handover on Google Pixel.
