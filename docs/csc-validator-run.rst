Run a Validator
===============================================================================

Hardware
-------------------------------------------------------------------------------

..code-block::bash
  
  CPU: 16Core
  RAM: 32GB
  HDD: SSD 1TB

Initialize
-------------------------------------------------------------------------------

Refer to Run a Node

Create Validator Address
-------------------------------------------------------------------------------

You need to create an account that represents a validator's consensus key for 
block signatures. Use the following command to create a new account and set a 
password for that account:

..code-block::bash

  docker run --interactive \
    --volume $PWD:/root \
    --workdir /root \
    genzbank/cetd \
      account new \
      --datadir /root
    
  genz-cetd-pool \
    staking init \
      --name=main \
      --network=test

Start Validator Node
-------------------------------------------------------------------------------

Save keyfile password of validator account in file

..code-block::bash
  
  echo "your password" > password.txt

Start mining

..code-block::bash
  
  docker run --interactive \
    --volume $PWD:/root \
    --workdir /root \
    genzbank/cetd \
      --datadir /root \
      --unlock "0x8Db808CDB8606F66399E92FCc2b1b349c43671A2" 
      --password /root/password.txt  \
      --mine  \
      --allow-insecure-unlock


