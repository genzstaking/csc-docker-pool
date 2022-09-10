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


def handle_validator_init(args):
    _logger.info("Start handling validator init command")
    client = load_docker()
    docker_get_or_create_network("csc")
    
    if args.force:
        node = load_node_with_name(args)
        if not node.is_initialized:
            node = create_node_with_name(args)
    else:
        node = create_node_with_name(args)
    
    options = "".join([
        " validator.create ",
        generate_keystore_options(node, args),
        generate_passowrd_file_options(node, args),
        generate_chain_options(node, args),
        #generate_logging_options(node, args),
        generate_validator_options(node, args),
        generate_relay_options(node, args),
        generate_metrics_options(node, args)
    ])
    
    # Create validator node
    _logger.debug("Options to run CETD : {}".format(options))
    _logger.info("Running ghcr.io/genz-bank/cetd container to init node {}".format(node.name))
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
        network="csc"
    )
    redirect_container_logs(container, args)
    
    _logger.info("Node {} is initialized with default configuration".format(node.name))
    node.is_initialized = True
    node.type = "csc-validator"
    node.save()
    return True


def handle_validator_list(args):
    root_path = os.getcwd()
    nodes = [ create_node(f.path) for f in os.scandir(root_path) if f.is_dir() and is_node(f.path) ]
    data = []
    for node in nodes:
        if node.type != "csc-validator":
            continue
        if docker_is_running(generate_validator_name(node)):
            node.state = 'Running'
        else:
            node.state = 'Stopped'
        data.append(node.__dict__)
    frame = pandas.DataFrame(data, columns=['id', 'name', 'type', 'network', 'is_initialized', 'state'])
    print(frame)


def handle_validator_start(args):
    _logger.info("Start handling validator init command")
    client = load_docker()
    
    node = load_node_with_name(args)
    
    options = "".join([
        generate_data_dir_options(node, args),
        generate_logging_options(node, args),
        generate_passowrd_file_options(node, args),
        generate_validator_addrress_options(node, args),
        " --allow-insecure-unlock ",
        " --mine "
    ])
    
    # Create validator node
    _logger.debug("Options to start CETD  validator : {}".format(options))
    _logger.info("Running ghcr.io/genz-bank/cetd container to start a validator {}".format(args.name))
    container = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        name=generate_validator_name(node, args),
        volumes=[node.path + ":/root"],
        working_dir="/root",
        auto_remove=True,
        remove=True,
        stderr=True,
        stdout=True,
        detach=True,
        network="csc",
    )
    redirect_container_logs(container, args)
    _logger.info("Node {} is initialized with default configuration".format(args.name))
    node.save()
    return True


def handle_validator_stop(args):
    _logger.info("Stops the validator node {}".format(args.name))
    node = create_node(os.getcwd() + '/' + args.name)
    client = load_docker()
    container_name = generate_validator_name(node, args)
    try:
        container = client.containers.get(container_name)
        container.remove(force=True)
    except docker.errors.NotFound:
        _logger.info("The validator not not exist")
        return False
    except docker.errors.APIError:
        _logger.critical(msg="Fail to load docker from environment. Check if it is installed and run")
        exit(1)


def handle_validator_edit(args):
    _logger.info("Start handling validator init command")
    client = load_docker()
    handle_validator_stop(args)
    
    node = load_node_with_name(args)
    node.load_from_args(args)
    
    if node.type != "csc-validator":
        _logger.error("This is not a validator node")
        exit(3)
    
    if not node.is_initialized:
        _logger.error("The node is not initialized")
        exit(3)
    
    options = "".join([
        " validator.edit ",
        generate_keystore_options(node, args),
        generate_passowrd_file_options(node, args),
        generate_chain_options(node, args),
        #generate_logging_options(node, args),
        generate_validator_options(node, args),
        generate_relay_options(node, args),
        generate_metrics_options(node, args)
    ])
    
    # Create validator node
    _logger.debug("Options to run CETD : {}".format(options))
    _logger.info("Running ghcr.io/genz-bank/cetd container to init node {}".format(node.name))
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
        network="csc",
    )
    redirect_container_logs(container, args)
    _logger.info("Node {} is initialized with default configuration".format(args.name))
    node.is_initialized = True
    node.save()



def handle_validator_info(args):
    """
    Inquire staking info from any address to node
    
    @param args: command line arguments
    """
    
    _logger.info("Start handling validator info command")
    client = load_docker()
    handle_validator_stop(args)
    
    node = load_node_with_name(args)
    
    if node.type != "csc-validator":
        _logger.error("This is not a validator node")
        exit(3)
    
    if not node.is_initialized:
        _logger.error("The node is not initialized")
        exit(3)
    
    # Descripiton
    options = "".join([
        " validator.description.query ",
        generate_validator_addresses_options(node, args),
        generate_relay_options(node, args),
    ])
    
    # Create validator node
    _logger.debug("Options to run CETD : \n {}".format(options))
    _logger.info("Running ghcr.io/genz-bank/cetd container to init node {}".format(node.name))
    output = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[node.path + ":/root"],
        working_dir="/root",
        auto_remove=True,
        stderr=True,
        stdout=True,
        detach=False,
        network="csc",
    )
    print(output.decode('utf-8'))
    
    
    # Info
    options = "".join([
        " validator.info.query ",
        generate_validator_addresses_options(node, args),
        generate_relay_options(node, args),
    ])
    
    # Create validator node
    _logger.debug("Options to run CETD : \n {}".format(options))
    _logger.info("Running ghcr.io/genz-bank/cetd container to init node {}".format(node.name))
    output = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[node.path + ":/root"],
        working_dir="/root",
        auto_remove=True,
        stderr=True,
        stdout=True,
        detach=False,
        network="csc",
    )
    print(output.decode('utf-8'))
    
    
    # slash
    options = "".join([
        " validator.slash.record ",
        generate_validator_addresses_options(node, args),
        generate_relay_options(node, args),
    ])
    
    # Create validator node
    _logger.debug("Options to run CETD : \n {}".format(options))
    _logger.info("Running ghcr.io/genz-bank/cetd container to init node {}".format(node.name))
    output = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[node.path + ":/root"],
        working_dir="/root",
        auto_remove=True,
        stderr=True,
        stdout=True,
        detach=False,
        network="csc",
    )
    print(output.decode('utf-8'))


def handle_validator_unjail(args):
    _logger.info("Start handling validator unjail command")
    client = load_docker()
    node = load_node_with_name(args)
    
    options = "".join([
        " unjail ", 
        generate_keystore_options(node, args),
        generate_passowrd_file_options(node, args),
        generate_validator_from_address_options(node, args),
        generate_relay_options(node, args),
    ])
    
    # Create validator node
    _logger.debug("Options to start CETD  validator : \n{}".format(options))
    _logger.info("Running ghcr.io/genz-bank/cetd container to start a validator {}".format(args.name))
    output = client.containers.run(
        image="ghcr.io/genz-bank/cetd",
        command=options,
        user=os.getuid(),
        volumes=[node.path + ":/root"],
        working_dir="/root",
        auto_remove=True,
        stderr=True,
        stdout=True,
        detach=False,
        network="csc",
    )
    print(output.decode('utf-8'))
    return True


def parse_args(subparsers):
    parser = subparsers.add_parser(
        'validator',
        help='Manages a staking node'
    )
    staking_parser = parser.add_subparsers(
        help="validator",
        title="Staking Nodes Management",
        description="""
        A staking (validator) node is responsible to generate new blocks.
        """,
        dest='command'
    )
    
    #---------- init
    # --name          <name, a key to list nodex>
    # --network
    # --reward-wallet <address or name>
    # --owners        <address ..>
    # --label         <string to show on pools>
    # --description   <Define the node>
    # --website       <homepage address>
    # --relay         <address of relay node>
    staking_init = staking_parser.add_parser(
        'init',
        help='Initialize a staking node'
    )
    staking_init.set_defaults(func=handle_validator_init)
    add_password_file_arguments(staking_init)
    add_name_arguments(staking_init)
    add_chain_arguments(staking_init)
    add_validator_arguments(staking_init)
    add_relay_arguments(staking_init)
    add_metric_arguments(staking_init)
    
    # -------------- Edit
    # Edit validator node
    # --name          <name, a key to list nodex>
    # --network
    # --reward-wallet <address or name>
    # --owners        <address ..>
    # --label         <string to show on pools>
    # --description   <Define the node>
    # --website       <homepage address>
    # --relay         <address of relay node>
    validator_edit = staking_parser.add_parser(
        'edit',
        help='Edit a validator node'
    )
    validator_edit.set_defaults(func=handle_validator_edit)
    add_password_file_arguments(validator_edit)
    add_name_arguments(validator_edit)
    add_chain_arguments(validator_edit)
    add_validator_arguments(validator_edit)
    add_relay_arguments(validator_edit)
    add_metric_arguments(validator_edit)
    
    # ----------- List
    validator_list = staking_parser.add_parser(
        'list',
        help='List all initialized validator node'
    )
    validator_list.set_defaults(func=handle_validator_list)
    
    # ----------- Start
    validator_start = staking_parser.add_parser(
        'start',
        help='Start a staking node'
    )
    validator_start.set_defaults(func=handle_validator_start)
    add_name_arguments(validator_start)
    add_password_file_arguments(validator_start)
    
    # ----------- Stop
    validator_stop = staking_parser.add_parser(
        'stop',
        help='Start a staking node'
    )
    validator_stop.set_defaults(func=handle_validator_stop)
    add_name_arguments(validator_stop)
    
    # ----------- Withdraw reward
    # cetd withdrawreward 
    #     --from 0x65804ab640b1d4db5733a36f9f4fd2877e4714ec 
    #     --validator.address 0x42eacf5b37540920914589a6b1b5e45d82d0c1ca 
    #     --keystore ./data/keystore/ 
    #     --node http://127.0.0.1:8545
        
    # ------------- Info
    validator_info = staking_parser.add_parser(
        'info',
        help='Inquire staking info from any address to node'
    )
    validator_info.set_defaults(func=handle_validator_info)
    add_relay_arguments(validator_info)
    add_name_arguments(validator_info)
    
    
    # ------------- Unjail
    # cetd unjail 
    #     --from 0x582bd2e02494dc6beb9a14401f4eae009533484c 
    #     --keystore ./data/keystore/ 
    #     --node http://127.0.0.1:8545
    validator_unjail = staking_parser.add_parser(
        'unjail',
        help='Unjail validator if validator is jailed'
    )
    validator_unjail.set_defaults(func=handle_validator_unjail)
    add_name_arguments(validator_unjail)
    add_relay_arguments(validator_unjail)
    add_password_file_arguments(validator_unjail)
    
