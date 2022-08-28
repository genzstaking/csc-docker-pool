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

    
def handle_staking_init(args):
    _logger.info("Start handling relay init command")
    client = load_docker()
    
    
    node = create_node_with_name(args)
    
    options = "".join([
        generate_data_dir_options(node, args),
        generate_chain_options(node, args),
        generate_logging_options(node, args),
        generate_staking_options(node, args),
        generate_relay_options(node, args),
        generate_metrics_options(node, args)
    ])
    
    # Create validator node
    _logger.debug("Options to run CETD : {}".format(options))
    _logger.info("Running ghcr.io/genz-bank/cetd container to init node {}".format(args.name))
    container = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[relay.path + ":/root"],
        working_dir="/root",
        auto_remove=True,
        remove=True,
        stderr=True,
        stdout=True,
        detach=True,
    )
    redirect_container_logs(container, args)
    
    _logger.info("Node {} is initialized with default configuration".format(args.name))
    relay.is_initialized = True
    relay.save()
    return True


def handle_staking_start(args):
    # cetd 
    #     --datadir /path/your-data-localtion-folder 
    #     --unlock "your validator address" 
    #     --password /path/your-keyfile-folder/password.txt  
    #     --allow-insecure-unlock
    #     --mine  
    return True


def handle_staking_stop(args):
    return True


def parse_args(subparsers):
    parser = subparsers.add_parser(
        'staking',
        help='Manages a staking node'
    )
    staking_parser = parser.add_subparsers(
        title="Staking Nodes Management",
        description="""
        A staking (validator) node is responsible to generate new blocks.
        """
    )
    
    #----------------------------------------------------------
    # init
    # --name          <name, a key to list nodex>
    # --network
    # --reward-wallet <address or name>
    # --owners        <address ..>
    # --label         <string to show on pools>
    # --description   <Define the node>
    # --website       <homepage address>
    # --relay         <address of relay node>
    #----------------------------------------------------------
    staking_init = staking_parser.add_parser(
        'init',
        help='Initialize a staking node'
    )
    staking_init.set_defaults(func=handle_staking_init)
    staking_init.add_argument(
        '--name',
        help='target wallet name',
        dest='name',
        default='main'
    )
    staking_init.add_argument(
        '--network',
        help='The name of the network (main, or test)',
        default='main',
        type=str,
        choices=['main', 'test'],
        required=False,
        dest='network'
    )
    staking_init.add_argument(
        '--reward-wallet',
        help='reward receiver of validator (default: validator\'s address)',
        type=str,
        required=False,
        dest='reward_wallet'
    )
    staking_init.add_argument(
        '--owners',
        help='transaction\'s from address',
        nargs=1,
        type=str,
        required=True,
        dest='owners'
    )
    staking_init.add_argument(
        '--label',
        help='Label of the node',
        type=str,
        required=False,
        dest='label'
    )
    staking_init.add_argument(
        '--description',
        help='description of the node',
        type=str,
        required=False,
        dest='description'
    )
    staking_init.add_argument(
        '--website',
        help='website of the node',
        type=str,
        required=False,
        dest='website'
    )
    staking_init.add_argument(
        '--relay',
        help='relay node to publish transactions',
        type=str,
        required=True,
        dest='relay'
    )
    add_metric_arguments(staking_init)
    
