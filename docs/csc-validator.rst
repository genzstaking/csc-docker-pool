CSC Validator
===============================================================================

CSC adopts 'CPoS' consensus and supports up to 101 validators. In order, each 
validator takes turn to generate blocks and validate block info of other 
validators.

How to become a validator
-------------------------------------------------------------------------------

Everyone can become validator by staking CET. Based on overall staking ranking, 
the blockchain will select the top 101 nodes as validators in every 200 blocks.

Our csc-docker-pool helps you to become a validator fast.

How to stake
-------------------------------------------------------------------------------

After launch, CSC will initialize the validator system contract. Staking is 
available for everyone via invoking the contract directly. The first staking
for the validator must exceed 10000 CET and each subsequent staking must exceed 
1000 CET. In addition to staking by invoking the contract directly, you can also 
stake via csc-docker-pool command line. 

More details of CSC Docker Pool CLI

TODO: maso, 2022: support wallet CLI

Rewards
-------------------------------------------------------------------------------

Mainly, the rewards for validators are from block rewards and tx fees. These 
rewards will be allocated according to the proportion of node staking in overall 
staking.

