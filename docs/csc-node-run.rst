Run a Node
===============================================================================

Hardware requirements
-------------------------------------------------------------------------------

Recommended resourse:

..code-block::bash

  CPU: 16Core
  RAM: 32GB
  HDD: SSD 1TB

But you can use:

..code-block::bash

  CPU: 8Core
  RAM: 16GB
  HDD: SSD 500GB

Network:

..code-block::bash

    Public network IP
    Open TCP/UDP port for P2P discovery and interconnection. Default P2P portal.
        Mainnet: 36652
        Testnet: 36653


Initialize
-------------------------------------------------------------------------------

Initialize command:

..code-block::bash

  genz-cetd-pool \
    relay init \
      --name=main


This command will create the data directory and keystore directory under 
/{name}, and create Genesis Block. If the default --name is 
not specified, it will create main as the data directory and 'keystore' 
directory in the current directory. As follows:


..code-block::bash

  ./main
    ├── cetd
    │   ├── chaindata
    │   │   ├── 000001.log
    │   │   ├── CURRENT
    │   │   ├── LOCK
    │   │   ├── LOG
    │   │   └── MANIFEST-000000
    │   ├── lightchaindata
    │   │   ├── 000001.log
    │   │   ├── CURRENT
    │   │   ├── LOCK
    │   │   ├── LOG
    │   │   └── MANIFEST-000000
    │   ├── LOCK
    │   └── nodekey
    └── keystore

By default, init command is initialized to Mainnet information. You can change
network by --network option. For example to init the a node for the testnet
execute the following command.

..code-block::bash

  genz-cetd-pool \
    relay init \
      --name=main \
      --network=test


Run
-------------------------------------------------------------------------------

The next step is to launch the node. Suppose you initialized a node successfully, to 
launch the node use the following command.


..code-block::bash

  genz-cetd-pool \
    relay run \
      --name=main


By default, the synchronization mode is fast, which can be changed to full mode 
with the option --syncmode full. We have assigned P2P seed Node in cetd by default. 

You can change and assign trusted Seed Nodes via --bootnodes options.

Now use the following command to list all initialized node:

..code-block::bash

  genz-cetd-pool \
    relay lsit

Configuration
-------------------------------------------------------------------------------

To make it easy for all users to deploy CSC nodes, we have integrated some default 
configuration into the binary package 'cetd' file so that everyone can start without 
any configuration. For professional users, you can refer to the following 
configuration, optimize the configuration, and then start the command as: cetd 
--config ./<your config file>

TODO: support custom config

eg：testnet config
assets/testnet.config
