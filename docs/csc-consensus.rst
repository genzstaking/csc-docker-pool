About CSC Consensus
===============================================================================

CoinEx Smart Chain (CSC) adopts CPoS consensus protocol and is fully compatible 
with Ethereum virtual machine (EVM) on support for high performance transactions, 
with a maximum capacity of up to 101 validators simultaneously. Meanwhile, CSC 
adheres to the principle of decentralization and permission-free so that anyone 
can become a validator by staking CET.

Goals of CSC
-------------------------------------------------------------------------------

* Shorter time period for block generation
* Higher compatibility with Ethereum
* Decentralization

CPoS Consensus
-------------------------------------------------------------------------------

Although Proof of Work (PoW) has been proved to be a practical solution for 
decentralized networks, yet it is not environment-friendly and requires a large 
number of participants to maintain network security.

On the other hand, Ethereum and some other networks use Proof of Authority (PoA) 
or its variants in different scenarios, including test network and main network. 
PoA provides defense for 51% attack and is more effective in preventing evil-doing 
by some Byzantine nodes. However, PoA protocol is not decentralized enough, for 
the validators are prone to corruption and security attacks given the extreme 
powers they possess.

Therefore, some blockchain projects introduce other consensus schemes on the premise 
of ensuring network security and stability without compromising decentralization, 
such as DPoS adopted by EOS and Cosmos, which allows token holders to vote for 
validator nodes and makes the blockchain more decentralized and conducive to 
community management.

After rigorous investigation and research, CoinEx Team adheres to the principle of 
decentralization and combines the characteristics of PoS with PoA to realize CPoS, 
without losing network stability and security. The features of CPoS are as follows:

* Blocks are generated with a maximum of 101 validator nodes.
* Anyone can become a validator by staking CET without any permitted.
* Validators take turns to generate blocks. When the validator node produce blocks normally, the difficulty is 2; when the validator node do not produce blocks in a predetermined order, the difficulty is reduced to 1; when the block forks, the chain with the greatest difficulty will be systematically selected.
* Anyone can stake for their trusted validator.
