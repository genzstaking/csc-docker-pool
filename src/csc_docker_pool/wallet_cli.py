import logging
import docker
import os
import codecs
from builtins import IOError, FileNotFoundError
import time
import pandas
import random

from csc_docker_pool.node import *
from csc_docker_pool.docker_util import *
from csc_docker_pool.args_util import *

_logger = logging.getLogger(__name__)


def handle_wallet_list(args):
    _logger.info("Getting list of wallets (accounts) in node {}".format(args.name))
    
    client = load_docker()
    node = load_node_with_name(args)
    # Command options
    options = "".join([
        "account  list ",
        generate_node_dir_options(node, args)
    ])
    
    _logger.info("Running ghcr.io/genz-bank/cetd container to list accounts")
    output = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[os.getcwd() + ":/root"],
        working_dir="/root",
    )
    print(output.decode('utf-8'))

def handle_wallet_new(args):
    _logger.info("Start handling wallet new command")
    client = load_docker()
    node = load_node_with_name(args)
    _logger.info("Getting list of wallets (accounts) in node {}".format(node.name))
        
    # Command options
    options = "".join([
        "account  new ",
        generate_node_dir_options(node, args),
        generate_passowrd_file_options(node, args),
    ])
    
    _logger.info("Running ghcr.io/genz-bank/cetd container to list accounts")
    container = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[os.getcwd() + ":/root"],
        working_dir="/root",
        stderr=True,
        stdout=True,
        detach=True,
    )
    redirect_container_logs(container, args)


def handle_wallet_import(args):
    _logger.info("Start handling wallet import command")
    client = load_docker()
    node = load_node_with_name(args)
    _logger.info("Getting list of wallets (accounts) in node {}".format(args.name))
    # Command options
    options = "".join([
        "account  list ",
        generate_node_dir_options(args),
        # XXX: maso, 2022: move key file into a volume
        args.keyfile
    ])
    
    _logger.info("Running ghcr.io/genz-bank/cetd container to list accounts")
    output = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[os.getcwd() + ":/root"],
        working_dir="/root",
    )
    print(output.decode('utf-8'))
    
def parse_args(subparsers):
    parser = subparsers.add_parser(
        'wallet',
        help='Manages wallets/accounts.'
    )

    wallet_parser = parser.add_subparsers(
        title="Wallet Management",
        description="""
        In CSC network wallets are called account so. This command manage list of accounts.
        """
    )
    
    #---------- list
    wallet_lsit = wallet_parser.add_parser(
        'list',
        help='To display list of created wallets'
    )
    wallet_lsit.set_defaults(func=handle_wallet_list)
    add_name_arguments(wallet_lsit)
    
    
    #---------- new
    wallet_new = wallet_parser.add_parser(
        'new',
        help='To create a new wallets'
    )
    wallet_new.set_defaults(func=handle_wallet_new)
    add_name_arguments(wallet_new)
    add_password_file_arguments(wallet_new)
    
    #----------- import
    wallet_import = wallet_parser.add_parser(
        'import',
        help = "Imports an unencrypted private key and creates a new account.",
        description="""
            Imports an unencrypted private key from <keyfile> and creates a new account.
            
            NOTE: As you can directly copy your encrypted accounts to another ethereum instance,
            this import mechanism is not needed when you transfer an account between
            nodes.
            """
    )
    wallet_import.set_defaults(func=handle_wallet_import)
    add_name_arguments(wallet_import)
    add_password_file_arguments(wallet_import)
    add_keyfile_arguments(wallet_import)

    #-------------- Stake
    # Stake for validator node
    #
    # cetd staking 
    #     --from 0x65804ab640b1d4db5733a36f9f4fd2877e4714ec 
    #     --validator.address 0x42eacf5b37540920914589a6b1b5e45d82d0c1ca 
    #     --validator.staking 10000000000000000000000 
    #     --keystore ./data/keystore/ 
    #     --node http://127.0.0.1:8545
    
    # ---------------- Unstake
    #
    # cetd unstaking 
    #     --from 0x65804ab640b1d4db5733a36f9f4fd2877e4714ec 
    #     --validator.address 0x42eacf5b37540920914589a6b1b5e45d82d0c1ca 
    #     --keystore ./data/keystore/ 
    #     --node http://127.0.0.1:8545
    
    

    # -------- Withdraw staking
    #
    # cetd withdrawstake 
    #     --from 0x65804ab640b1d4db5733a36f9f4fd2877e4714ec 
    #     --validator.address 0x65804ab640b1d4db5733a36f9f4fd2877e4714ec 
    #     --keystore ./data/keystore/ 
    #     --node http://127.0.0.1:8545
