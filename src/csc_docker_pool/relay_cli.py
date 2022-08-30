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


def handle_relay_init(args):
    #----- Load tools
    _logger.info("Start initialization of a relay node")
    client = load_docker()
    node = create_node_with_name(args)
    
    #----- Generates options
    options = "".join([
        generate_data_dir_options(node, args),
        generate_chain_options(node, args),
        'init',
        generate_logging_options(node, args),
    ])
    
    #----- Run a docker
    _logger.debug("Command cetd {}".format(options))
    _logger.info("Running ghcr.io/genz-bank/cetd container to init node {}".format(args.name))
    container = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[node.path + ":/root"],
        working_dir="/root",
        auto_remove=True,
        remove=True,
        stderr=True,
        stdout=True,
        detach=True,
    )
    redirect_container_logs(container, args)
    
    #----- Save changes
    _logger.info("Node {} is initialized with default configuration".format(args.name))
    node.is_initialized = True
    node.type = "csc-realy"
    node.save()


def handle_relay_stop(args):
    _logger.info("Stops the relay node {}".format(args.name))
    node = create_node(os.getcwd() + '/' + args.name)
    client = load_docker()
    container_name = generate_relay_name(node, args)
    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
    except docker.errors.NotFound:
        _logger.info("The relay not not exist")
        return False
    except docker.errors.APIError:
        _logger.critical(msg="Fail to load docker from environment. Check if it is installed and run")
        exit(1)


def handle_relay_run(args):
    _logger.info("Running the relay node {}".format(args.name))
    relay = create_node(os.getcwd() + '/' + args.name)
    check_node_initialized(relay)
    client = load_docker()
    
    options = "".join([
        generate_data_dir_options(relay, args),
        generate_bootnodes_options(relay, args),
        generate_syncmod_options(relay, args),
        generate_metrics_options(relay, args),
        generate_rpc_http_options(relay, args)
    ])

    _logger.info("Running ghcr.io/genz-bank/cetd container for node {}".format(args.name))
    if docker_is_running(generate_relay_name(relay)):
        handle_relay_stop(args)
    port = get_option_value(relay, args, 'port')
    container = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        name=generate_relay_name(relay),
        user=os.getuid(),
        volumes=[relay.path + ":/root"],
        working_dir="/root",
        restart_policy={
            'Name': 'on-failure',
            'MaximumRetryCount': 10
        },
        ports = {
            port+'/tcp':port,
            port+'/udp':port
        },
        # auto_remove=True,
        #remove=True,
        stderr=True,
        stdout=True,
        detach=True,
    )
    relay.save()
    redirect_container_logs(container, args)


def handle_relay_list(args):
    root_path = os.getcwd()
    nodes = [ create_node(f.path) for f in os.scandir(root_path) if f.is_dir() and is_node(f.path) ]
    data = []
    for node in nodes:
        if docker_is_running(generate_relay_name(node)):
            node.state = 'Running'
        else:
            node.state = 'Stopped'
        data.append(node.__dict__)
    frame = pandas.DataFrame(data, columns=['id', 'name', 'type', 'network', 'is_initialized', 'state'])
    print(frame)


def parse_args(subparsers):
    parser = subparsers.add_parser(
        'relay',
        help='Manages a relay node'
    )
    relay_parser = parser.add_subparsers(
        title="Relay Nodes Management",
        description="""
        A relay node sync DB with the network.
        On the other hand, a relay node is an edge node and connects to other nodes on the
        network. It fetch/push new blocks and keeps the ledger update.
        This command helps you to setup, manage and maintain a node over the network.
        You may have multiple relay node at the same time, where each of which deals with 
        and specific network. For example a node to keeps testnet data."""
    )
    
    #---- init
    subparsers_init = relay_parser.add_parser(
        'init',
        help='Initialize the relay node'
    )
    subparsers_init.set_defaults(func=handle_relay_init)
    add_chain_arguments(subparsers_init)
    add_name_arguments(subparsers_init)
    add_metric_arguments(subparsers_init)
    
    #---- run
    subparsers_run = relay_parser.add_parser(
        'run',
        help='Run the relay node'
    )
    subparsers_run.set_defaults(func=handle_relay_run)
    add_name_arguments(subparsers_run)
    add_metric_arguments(subparsers_run)
    # TODO: maso, 2022: Map these options to abstract models
    add_syncmode_arguments(subparsers_run)
    add_bootnodes_arguments(subparsers_run)
    
    #------ stop
    relay_stop = relay_parser.add_parser(
        'stop',
        help='Stop a relay node'
    )
    relay_stop.set_defaults(func=handle_relay_stop)
    add_name_arguments(relay_stop)

    #------ list
    subparsers_lsit = relay_parser.add_parser(
        'list',
        help='To display list of created relay nodes'
    )
    subparsers_lsit.set_defaults(func=handle_relay_list)



#
# Inquire validator description info
#
# cetd validator.description.query 
#     --validator.address 0x65804ab640b1d4db5733a36f9f4fd2877e4714ec 
#     --node http://127.0.0.1:8545
#
#
# Inquire node info such as block generation, reward, etc
#
# cetd validator.info.query 
#     --validator.address 0x65804ab640b1d4db5733a36f9f4fd2877e4714ec 
#     --node http://127.0.0.1:8545
#
#
# Inquire activated node list
#
# cetd validator.activated.query 
#     --node http://127.0.0.1:8545
#
#
# Inquire candidate node list
#
# cetd validator.candidators.query 
#     --node http://127.0.0.1:8545
