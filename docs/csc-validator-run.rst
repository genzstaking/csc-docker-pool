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



init 

genz-cetd-pool -vv --force validator init \
    --name validator \
    --relay relay \
    --owner-wallet 0x65ac59248995b86dfebd27b0707e24327a359ec4 \
    --reward-wallet 0x3a4f8dfe9bb0e33a492487161a23187fef2db11e \
    --label test \
    --description "a test node" \
    --website "http://test.com" \
    --email "info@test.com"
    
Start mining

genz-cetd-pool -vv validator start \
    --name validator \
    --password 1234


genz-cetd-pool -vv validator stop \
    --name validator

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


